# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 22:35:43 2024

@author: edobo
"""

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
#import datasets
mocarelli = pd.read_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Mocarelli\mocarelli_clean.xlsx", header = 0)
ogilvie_path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Ogilvie\Database_for_Italy_ogilvie.xlsx"
ogilvie = pd.read_excel(ogilvie_path)

#upper the names in mocarelli and ogilvie
mocarelli['guild_name'] = mocarelli['guild_name'].str.upper()
mocarelli['Translation of name'] = mocarelli['Translation of name'].str.upper()
ogilvie['guild_name'] = ogilvie['guild_name'].str.upper().str.rstrip()

#drop nan
ogilvie = ogilvie.dropna(subset = 'guild_name')

#create list of name
ogilvie_names = ogilvie['guild_name'].unique()
mocarelli_names = mocarelli['guild_name'].unique()



#create the first basic dictionary
#fix manually the "rimasugli" column
ogilvie[['guild_name', 'guild_name_ITA', 'rimasugli']] = ogilvie['guild_name'].str.split("(", expand=True)
ogilvie['guild_name_ITA'] = ogilvie['guild_name_ITA'].str.replace('(', '').str.replace(')', '').str.replace(',', ' ')
ogilvie_translation = [(row['guild_name'], row['guild_name_ITA']) for key, row in ogilvie.iterrows()]
ogilvie_translation_dict  = list_to_dict(ogilvie_translation)
ogilvie_translation_dict = {key : [value for value in values if not isinstance(value, type(None))] 
                            for key, values in ogilvie_translation_dict.items()}
ogilvie_translation_dict = {key : value for key, value in ogilvie_translation_dict.items() if not len(value) == 0}
#clean the strings
ogilvie_translation_dict = {key : [value.replace('(' , '').replace(')', '') for value in values] for key, values in 
                            ogilvie_translation_dict.items()}
ogilvie['guild_name_ITA'] = ogilvie['guild_name'].map(ogilvie_translation_dict)

#use the mocarelli translation
mocarelli_senato_path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merge_senato_mocarelli_ADJUSTED.xlsx"
mocarelli_senato = pd.read_excel(mocarelli_senato_path)
mocarelli_senato['Occupation'] = mocarelli_senato['Occupation'].str.upper()
mocarelli_translation = [(row['Occupation'], row['guild_name']) for key, row in mocarelli_senato.iterrows()]
mocarelli_translation_dict = list_to_dict(mocarelli_translation)
mocarelli_translation_dict = {key : list(set(value)) for key, value in mocarelli_translation_dict.items()}
mocarelli_translation_inverted = [(row['guild_name'], row['Occupation']) for key, row in mocarelli_senato.iterrows()]
mocarelli_translation_dict_inverted = list_to_dict(mocarelli_translation_inverted)
ogilvie['guild_name_ITA_mocarelli'] = ogilvie['guild_name'].map(mocarelli_translation_dict)
mocarelli_results = ogilvie['guild_name_ITA_mocarelli'].count()

#try to use mocarelli's translation(from Translation of name)
name_translation = [(row['Translation of name'], row['guild_name']) for key, row in mocarelli.iterrows()]
name_translation = list_to_dict(name_translation)
ogilvie['guild_name_ITA_mocarelli_1'] = ogilvie['guild_name'].map(name_translation)

#try to enrich our translator
#try to see if other papers have relevant information
#import translator from paper of Lombardo 2001
translator_path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\dictionary_translator.xlsx"
translator = pd.read_excel(translator_path)
#upper the name
translator['guild_name'] = translator['guild_name'].str.upper().str.rstrip()
translator['guild_name_ITA'] = translator['guild_name_ITA'].str.upper().str.rstrip()
#obtain the dictionary. This will be a 1 key, plural values dictionary
translator_list = list(set([(row['guild_name'], row['guild_name_ITA']) for key, row in translator.iterrows()]))
translator_dict = list_to_dict(translator_list)
ogilvie['guild_name_ITA_lombardo'] = ogilvie['guild_name'].map(translator_dict)

final_translator = merge_dict(translator_dict, name_translation)
final_translator = merge_dict(final_translator, ogilvie_translation_dict)
final_translator = merge_dict(final_translator, mocarelli_translation_dict)
final_translator = {key : list(set(value)) for key, value in final_translator.items()}
ogilvie['guild_name_ITA_all'] = ogilvie['guild_name'].map(final_translator)
not_nan_f = ogilvie['guild_name_ITA_all'].count()

#Now we have the translator from English to Italian that translate every english ogilvie name in a "list" of italian names
place_mapping = {'VENICE': 'VENEZIA', 'MILAN': 'MILANO', 'FLORENCE': 'FIRENZE',
                 'GENOA' : 'GENOVA', 'ROME' : 'ROMA', 'TURIN' : 'TORINO', 'PALERMO' : 'PALERMO',
                 'BOLOGNA' : 'BOLOGNA', 'SYRACUSE' : 'SIRACUSA', 'PADUA' : 'PADOVA', 'MANTUA' : 'MANTOVA', 'NAPLES' : 'NAPOLI', 
                 'CAGLIARI':'CAGLIARI', 'ALGHERO' : 'ALGHERO', 'CATANIA' : 'CATANIA'}

ogilvie['place'] = ogilvie['place'].apply(lambda x: next((value for key, value in place_mapping.items() if key in x), x))

dict_path = r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\translator.json'
with open(dict_path, 'w') as json_file:
    json.dump(final_translator, json_file)

#final adjustments
columns = ogilvie.columns.to_list()
columns = columns[0:8] + columns[194:200] + columns[8:194]
ogilvie = ogilvie[columns]
ogilvie.to_excel(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\ogilvie_translation.xlsx')

