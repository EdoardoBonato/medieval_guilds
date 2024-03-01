# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 18:54:03 2024

@author: edobo
"""
import PyPDF2
import pandas as pd
import numpy as np
from collections import defaultdict
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import math
import sys
import json
sys.path.append(r"C:\Users\edobo\OneDrive\Desktop\Python\modules")
from data_structures import list_to_dict
from data_structures import merge_dict
from statistical_calculations import frequencies

path_merged = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\final_merging_attempt.xlsx"
merged = pd.read_excel(path_merged)

#to translate
merged_translate = merged[pd.isna(merged['GuildsID'])]
merged_translate = merged[pd.isna(merged['guild_name'])]
list_to_exclude = ['VARIOUS GUILDS', 'ALL GUILDS', 'ALL GUILDED OCCUPATIONS', 'ALL OCCUPATIONS', 
                   'UNSPECIFIED GUILDED OCCUPATIONS', 'UNSPECIFIED OCCUPATIONS', 'ALL OCCUPTION EXCEPT BUTCHERS'
                   ]
merged_translate = merged_translate[~merged_translate['guild_name_eng'].isin(list_to_exclude)]
group = merged_translate.groupby(['guild_name_eng', 'place'])
guilds_names = group.groups.keys()

path = r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\translator.json'
with open(path, 'r') as json_file:
    imported_dict = json.load(json_file)

#modify the dictionary
imported_dict_ed = {key: value[0] if len(value) ==1 else value for key, value in imported_dict.items() }
merged_translate['guild_name_eng_ITA'] = merged_translate['guild_name_eng'].map(imported_dict_ed)

#further check on correspondence
model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v1')
#embedd ogilvie missing
ogilvie_names = [(row['place'], row['guild_name_eng_ITA']) for key, row in merged_translate.iterrows()]
ogilvie_names_dict = list_to_dict(ogilvie_names)
ogilvie_names_dict = {key : value for key, value in ogilvie_names_dict.items() if not len(value) == 0}
embedded_ogilvie = [(key,model.encode(valuex)) for key,value in ogilvie_names_dict.items() for valuex in value if isinstance(valuex, str)]
ogilvie_new_names_dict = [(key, valuex) for key, value in ogilvie_names_dict.items() for valuex in value if isinstance(valuex, str)]
ogilvie_new_names_dict = list_to_dict(ogilvie_new_names_dict)
embedded_ogilvie_dict = list_to_dict(embedded_ogilvie)

#embedd mocarelli
merged_not_translated = merged.dropna(subset = 'GuildsID')
merged_not_translated = merged.dropna(subset = 'guild_name')
merged_not_translated = merged_not_translated[~merged_not_translated['guild_name_eng'].isin(list_to_exclude)]

merged_names = [(row['place'], row['guild_name']) for key, row in merged_not_translated.iterrows()]
merged_names_dict = list_to_dict(merged_names)
merged_names_dict = {key : value for key, value in merged_names_dict.items() if not len(value) == 0}
embedded_merged = [(key,model.encode(valuex)) for key,value in merged_names_dict.items() for valuex in value if isinstance(valuex, str)]
merged_new_names_dict = [(key, valuex) for key, value in merged_names_dict.items() for valuex in value if isinstance(valuex, str)]
merged_new_names_dict = list_to_dict(merged_new_names_dict)
embedded_merged_dict = list_to_dict(embedded_merged)

similarities = []
for place_mo, embedding_mo in embedded_merged_dict.items():
    for place_og, embedding_og in embedded_ogilvie_dict.items():
        if place_mo == place_og:
            merged_values = merged_new_names_dict[place_mo]
            ogilvie_values = ogilvie_new_names_dict[place_og]
            for index , value in enumerate(embedding_mo):
                    embedding = value.reshape(1, -1)
                    gilda = merged_values[index]
                    for n, valuex in enumerate(embedding_og):
                        valuex = valuex.reshape(1, -1)
                        embedded = np.append(embedding, valuex, axis = 0)
                        similarity = cosine_similarity(embedded)
                        gilda_og = ogilvie_values[n]
                        similarities.append((place_mo, gilda, gilda_og, similarity))
                        
similarities_08 = [(similarity[0], similarity[1], similarity[2], similarity[3][0]) for similarity in similarities]
positions = []
for n, elements in enumerate(similarities_08):
    indices = np.where(elements[3] > 0.8)
    if len(indices[0]) != 1:
        index = indices[0]
        positions.append((elements[0],elements[1], elements[2], index))
