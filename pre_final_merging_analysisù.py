# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 20:12:09 2024

@author: edobo
"""

import pandas as pd
import numpy as np
import xlsxwriter
import json
import numpy as np
import math
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import sys
sys.path.append(r"C:\Users\edobo\OneDrive\Desktop\Python\modules")
from data_structures import list_to_dict
from data_structures import merge_dict
from statistical_calculations import frequencies
import ast

ogilvie_translation_path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\ogilvie_translation_advanced.xlsx"
ogilvie = pd.read_excel(ogilvie_translation_path)
mocarelli_senato = pd.read_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merge_senato_mocarelli_ADJUSTED.xlsx")

place_mapping = {'VENICE': 'VENEZIA', 'MILAN': 'MILANO', 'FLORENCE': 'FIRENZE',
                 'GENOA' : 'GENOVA', 'ROME' : 'ROMA', 'TURIN' : 'TORINO', 'PALERMO' : 'PALERMO',
                 'BOLOGNA' : 'BOLOGNA', 'SYRACUSE' : 'SIRACUSA', 'PADUA' : 'PADOVA', 'MANTUA' : 'MANTOVA', 'NAPLES' : 'NAPOLI', 
                 'CAGLIARI':'CAGLIARI', 'ALGHERO' : 'ALGHERO', 'CATANIA' : 'CATANIA'}

#trying to merge using text analysis
#the idea is to run through every guild_name in Mocarelli, see if 
#there is a correspondence in the Ogilvie italian names.
#to do this it is useful to have dictionary with place, name of guild and embedded values

#embedding mocarelli 
model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v1')
mocarelli_names = [(row['place'], row['guild_name']) for key, row in mocarelli_senato.iterrows()]
mocarelli_names_dict = list_to_dict(mocarelli_names)
embedded_mocarelli = [(key, model.encode(value)) for key, value in mocarelli_names_dict.items()]
embedded_mocarelli_dict = list_to_dict(embedded_mocarelli)

#prepare ogilvie translated

ogilvie_translation = pd.read_excel(ogilvie_translation_path)
ogilvie_translation['place'] = ogilvie_translation['place'].apply(lambda x: next((value for key, value in place_mapping.items() if key in x), x))
ogilvie_names = [(row['place'], ast.literal_eval(row['guild_name_ITA_all'])) for key, row in ogilvie_translation.iterrows() if isinstance(row['guild_name_ITA_all'], str)]
ogilvie_names_dict = list_to_dict(ogilvie_names)

#embedding the name to see similarity with mocarelli

embedded_ogilvie = [(key,model.encode(valuex)) for key,value in ogilvie_names_dict.items() for valuex in value]
embedded_ogilvie = []
for key ,value in ogilvie_names_dict.items():
    for valuex in value:
        encoded = model.encode(valuex)
        embedded_ogilvie.append((key, encoded))
embedded_ogilvie_dict = list_to_dict(embedded_ogilvie)

#check whether there are similarities
similarities = []
for place_mo, embedding_mo in embedded_mocarelli_dict.items():
    for place_og, embedding_og in embedded_ogilvie_dict.items():
        if place_mo == place_og:
            mocarelli_values = mocarelli_names_dict[place_mo]
            ogilvie_values = ogilvie_names_dict[place_og]
            for index , value in enumerate(embedding_mo[0]):
                    embedding = value.reshape(1, -1)
                    gilda = mocarelli_values[index]
                    for n, valuex in enumerate(embedding_og):
                        embedded = np.append(embedding, valuex, axis = 0)
                        similarity = cosine_similarity(embedded)
                        gilda_og = ogilvie_values[n]
                        similarities.append((place_mo, gilda, gilda_og, similarity))

similarities_08 = [(array[0], array[1], array[2], array[3][0]) for array in similarities]
positions = []
for n, elements in enumerate(similarities_08):
    indices = np.where(elements[3] > 0.8)
    if len(indices[0]) != 1:
        index = indices[0]
        positions.append((elements[0],elements[1], elements[2], elements[3], index))
'''
positiona = []
for n, elements in enumerate(positions):
    positiones = elements[4][1]
    positiona.append(positiones)
    correspondence = elements[2][1]
    print(correspondence)
'''
        
path = r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\translator.json'
with open(path, 'r') as json_file:
    imported_dict = json.load(json_file)

elements = {}
for element in positions:
    elements[element[1]] = element[2]

eng_name = []
for key, value in imported_dict.items():
    for key1, value1 in elements.items():
            if value1 == value:
                eng_name.append((key, key1))
                
                
#it seems to be a relevant correspondence, use the corrresponding name to map italian name into ogilvie data
#final_dict = list_to_dict(similarities_)
#ogilvie['guild_name_ITA_both'] = ogilvie['guild_name'].map(final_dict)