import json
import csv


with open("./out_dict_base_own_mod_methanation.json") as f:
    label_data_own = json.load(f)

with open("./out_dict_base_mod_methanation.json") as f:
    label_data_base = json.load(f)

recall_base = [label_data_base[i]["recall"] for i in label_data_base]
recall_own = [label_data_own[i]["recall"] for i in label_data_own]

prec_base = [label_data_base[i]["precision"] for i in label_data_base]
prec_own = [label_data_own[i]["precision"] for i in label_data_own]

stdev_base = [label_data_base[i]["st_dev"] for i in label_data_base]
stdev_own = [label_data_own[i]["st_dev"] for i in label_data_own]

base = zip(list(label_data_base.keys()),recall_base,prec_base,stdev_base, recall_own, prec_own,stdev_own)

with open("metrics_methanation.csv", 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(base)