# -*- coding: utf-8 -*-
#this file clean the raw file(last version) BEFORE adjustment
#it produces 1897 different guilds
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

path_merged = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\final_merging_attempt_raw1.xlsx"
merged = pd.read_excel(path_merged)

#to translate

list_to_exclude = ['VARIOUS GUILDS', 'ALL GUILDS', 'ALL GUILDED OCCUPATIONS', 'ALL OCCUPATIONS', 
                   'UNSPECIFIED GUILDED OCCUPATIONS', 'UNSPECIFIED OCCUPATIONS', 'ALL OCCUPATIONS EXCEPT BUTCHERS',
                   'VARIOUS OCCUPATIONS'
                   ]
merged = merged[~merged['guild_name_eng'].isin(list_to_exclude)]


merged.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merged_clean1.xlsx")

group = merged.groupby(['guild_name_eng', 'place'])
guilds_names = group.groups.keys()
merged_translate = merged[pd.isna(merged['GuildsID'])]
merged_translate = merged[pd.isna(merged['guild_name'])]
#path = r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\translator.json'
#with open(path, 'r') as json_file:
#    imported_dict = json.load(json_file)

merged.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merged_clean1.xlsx")
