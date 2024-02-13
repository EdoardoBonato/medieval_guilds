# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 11:10:37 2024

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

path_merged = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merged_clean1_adj.xlsx"
merged = pd.read_excel(path_merged)
list_name = [(row['guild_name_eng'], row['guild_name']) for ket, row in merged.iterrows()]
dict_name = list_to_dict(list_name)
dict_name = {key : value for key, value in dict_name.items() if len(value) > 0}
rome = merged[merged.place == 'ROMA']
mask = rome['guild_name'].isna()

#modify the dictionary
dict_name = {key: value[0] for key, value in dict_name.items() }

rome[mask]['guild_name'] = rome[mask]['guild_name_eng'].map(dict_name)