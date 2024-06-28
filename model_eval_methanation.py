# -*- coding: utf-8 -*-

from text_mining import load_classes_chebi, delete_files_in_directory, run_text_mining, add_publication, text_prep, CatalysisIE_search
from preprocess_onto import *
from onto_extension_new import preprocess_classes,create_classes_onto
from txt_extract import get_abstract, get_metadata
from CatalysisIE.model import *
from CatalysisIE.utils import *
from pubchempy import get_compounds

import statistics
import json

import pybliometrics
pybliometrics.scopus.init()


def set_config_key(key, value):
    globals()[key] = value

def find_id_by_text(nested_list, search_text):
    for item in nested_list:
        if search_text in item["data"]["text"]:
            return nested_list.index(item)#["id"]
    return None

def id_from_abstr_snippet(nested_list, search_text):
    for i in range(len(abstract), 15, -1):
        res = find_id_by_text(label_data, abstract[1:i])
        if res is not None:
            return res
    return None


with open("config.json") as json_config:
    for key, value in json.load(json_config).items():
        set_config_key(key, value)

# TODO: Checkpoint dynamisch einbauen!
ckpt_name = "CatalysisIE/checkpoint/train_demo1_checkpoint-v4.ckpt"
#ckpt_name = "CatalysisIE/checkpoint/CV_0.ckpt"
model = BERTSpan.load_from_checkpoint(ckpt_name, model_name=bert_name, train_dataset=[], val_dataset=[], test_dataset=[])

out_dict = {}
label_list = ["Reactant","Product", "Characterization","Reaction","Catalyst","Treatment"]


with open("./methanation-manual_labels.json", encoding='utf-8') as f:
    label_data = json.load(f)

for i in glob.iglob(path):
    abstract = None
    try:
        title, doi, publisher = get_metadata(i)
    except:
        print("Metadata not found for {}".format(i))

    if doi == None:
        continue
    print(title+' : '+doi)
    abstract = get_abstract(i, doi, publisher)
    if abstract != None:
        #p_id = add_publication(doi,title,abstract)
        #if p_id == None:
        #    print('p_id = None')
        #    continue
        sents = text_prep(abstract)
        categories, chem_list, reac_dict, sup_cat, abbreviation, raw_entities = CatalysisIE_search(model, sents)

        entry_annotation_lst = id_from_abstr_snippet(label_data,abstract)
        if entry_annotation_lst == None:
            print("PROBLEM WITH fetched ABSTRACT! Check for misplaced characters like ﬁ instead of fi")
            print(abstract[1:40])
        label_dict_manual = {i: 0 for i in label_list}
        label_dict_model = {i: 0 for i in label_list}
        word_list_man = []
        word_list_mod = []

        label_man_index = {}

        out_dict[entry_annotation_lst] = []
        """
        out_dict = {1: {man: int, man_labels: {label1 : int, label2: int...}, model_name: int, model_name_labels: {label1:int, label2:int,...}, ...}, {2:...},...}
        """

        # Searches for similar entries in manually annotated and automatically annotated data
        for item in label_data[entry_annotation_lst]["annotations"][0]["result"]:
            label_dict_manual[item["value"]["labels"][0]] += 1
            word_list_man.append(item["value"]["text"])

            label_man_index[item["value"]["text"]] = item["value"]["labels"][0]

            category_keys = categories.keys()
            #list(set(, chem_list))

            if item["value"]["text"].rstrip('s') in [s.rstrip('s') for s in category_keys]:
                try:
                    if categories[item["value"]["text"]] == item["value"]["labels"][0]:
                        # contained in both manually and automatically labeled data
                        label_dict_model[item["value"]["labels"][0]] += 1
                        word_list_mod.append(item["value"]["text"])
                except:
                    if categories[item["value"]["text"].rstrip('s')] == item["value"]["labels"][0]: # try again without trailing s in model-labeled data
                        # contained in both manually and automatically labeled data
                        label_dict_model[item["value"]["labels"][0]] += 1
                        word_list_mod.append(item["value"]["text"])

        for i in chem_list:
            if i not in word_list_mod:# and i in list(label_man_index.keys()):
                    try:
                        print("Adding '{}' with label {}".format(i,label_man_index[i]))
                        label_dict_model[label_man_index[i]] += 1
                        word_list_mod.append(i)
                    except:
                        word_list_mod.append(i)

                        # Token detected without classification -> subsuming acc. to Fig 2 of Zhang et al. https://github.com/nsndimt/CatalysisIE/blob/main/JCIM2022.pdf
                        if label_dict_model["Catalyst"] != label_dict_manual["Catalyst"]:
                            label_dict_model["Catalyst"] += 1
                            print("Correct label for '{}' not clear. Assumed as Catalyst".format(i))

                        elif label_dict_model["Product"] != label_dict_manual["Product"]:
                            label_dict_model["Product"] += 1
                            print("Correct label for '{}' not clear. Assumed as Product".format(i))

                        elif label_dict_model["Reactant"] != label_dict_manual["Reactant"]:
                            label_dict_model["Reactant"] += 1
                            print("Correct label for '{}' not clear. Assumed as Reactant".format(i))

                        elif label_dict_model["Reaction"] != label_dict_manual["Reaction"]:
                            label_dict_model["Reaction"] += 1
                            print("Correct label for '{}' not clear. Assumed as Reaction".format(i))

                        elif label_dict_model["Characterization"] != label_dict_manual["Characterization"]:
                            label_dict_model["Characterization"] += 1
                            print("Correct label for '{}' not clear. Assumed as Characterization".format(i))

                        else:
                            label_dict_model["Treatment"] += 1
                            print("Correct label for '{}' not clear. Assumed as Treatment".format(i))
            else:
                print("Correct label for '{}' not clear, entry omitted.".format(i))


        num_lab_man = len(set(word_list_man))
        num_lab_mod = len(set(word_list_mod))

        recall = num_lab_mod/num_lab_man

        prec_classes = []
        for lab_class in list(label_dict_manual.keys()):
            if label_dict_manual[lab_class] !=0:
                prec_classes.append(label_dict_model[lab_class]/label_dict_manual[lab_class])

        deviation = statistics.stdev(prec_classes)
        prec = sum(prec_classes)/len(prec_classes)
        out_dict[entry_annotation_lst] = {"man": num_lab_man, "man_labels": label_dict_manual, "base_model": num_lab_mod, "base_model_labels":label_dict_model, "recall": recall, "precision": prec, "st_dev": deviation, "doi": doi, "token_man":label_man_index,"token_mod":list(set(word_list_mod)), "abstract": abstract}

    with open("./out_dict_base_own_mod_methanation.json",'w') as f:
        json.dump(out_dict, f)


