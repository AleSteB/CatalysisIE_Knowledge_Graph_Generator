# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 17:23:40 2024

@author: smaxbehr
"""

import json
from collections import Counter

with open("./project_new1.json") as f:
    data = json.load(f)
    

label_list = ["Reactant","Product", "Characterization","Reaction","Catalyst","Treatment"]

manual_count = {18:12, 19: 15, 20: 15, 21:0}
    
for pub_no in range(len(data)):
    
   # if pub_no == 18:
        
    try: 
        #num_res0 = len(data[pub_no]["annotations"][0]["result"])
        #num_res1 = len(data[pub_no]["annotations"][1]["result"])
        word_list_man = []
        word_list_1 = []
        word_list_2 = []
        
        #num_res2 = len(data[pub_no]["annotations"][2]["result"])
        label_dict_manual = {i:0 for i in label_list}
        label_dict_1 = {i:0 for i in label_list}
        label_dict_2 = {i:0 for i in label_list}
        
        for i in data[pub_no]["annotations"][0]["result"]:
            label_dict_manual[i["value"]["labels"][0]] += 1 
            word_list_man.append(i["value"]["text"])
                        
        for i in data[pub_no]["annotations"][1]["result"]:
            label_dict_1[i["value"]["labels"][0]] += 1 
            word_list_1.append(i["value"]["text"])
            
        for i in data[pub_no]["annotations"][2]["result"]:
            label_dict_2[i["value"]["labels"][0]] += 1 
            word_list_2.append(i["value"]["text"])
            
        pr_key_1 = []
        pr_key_2 = []
        #cnt = 0
        for key in label_list:
            if label_dict_manual[key] != 0:
                pr_key_1.append(label_dict_1[key]/label_dict_manual[key])
                pr_key_2.append(label_dict_2[key]/label_dict_manual[key])
                #cnt +=1
                
                #pr_key_2
        pr_1 = sum(pr_key_1)/len(pr_key_1)
        pr_2 = sum(pr_key_2)/len(pr_key_2)
        
        num_res0 = len(set(word_list_man))
        num_res1 = len(word_list_1)
        num_res2 = len(word_list_2)
        Rec_1 = num_res1/num_res0
        Rec_2 = num_res2/num_res0
        
        s_man = Counter(word_list_man)
        s_1 = Counter(word_list_1)
        s_2 = Counter(word_list_2)
            
        
        tp_1 = s_1 & s_man
        tp_2 = s_2 & s_man
        #"{:.2f}".format(a)
        print(str(pub_no) + ': TP+FN ' + str(num_res0))
        print('TP1: '+str(num_res1) +  ', R1: '+ '{:.3f}'.format(Rec_1)+ ', TP1: '+ str(len(tp_1)))
        print('TP2: '+str(num_res2) +  ', R2: '+ '{:.3f}'.format(Rec_2)+', TP2: '+ str(len(tp_2)) + '\n')
        #print(str(pub_no) + ': ' + str(num_res0) + ', '+str(num_res1) + ', '+ str(num_res2)+', Rec: '+str(Rec)+', Pr_1: '+str(pr_1) + ', Pr_2: '+str(pr_2))
        
    except:
        pass
    
    
    
    
  
    
    