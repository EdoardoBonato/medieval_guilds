# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 14:06:37 2024

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
from text_analysis import find_similarity
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import random

path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\final_merging_attempt.xlsx"

merged = pd.read_excel(path)


grouped = merged.groupby(['place', 'guild_name'])

grouped_min = grouped.agg({'combined_years' : 'min'})
grouped_min = grouped_min.reset_index()
mestieri= frequencies(grouped_min['guild_name'])
#type of mestieri
mestieri = mestieri.reset_index()
mestieri = mestieri.rename(columns = {'index' : 'guild_name'})

#embedding MERGED MESTIERI
model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v1')
mestieri_name = mestieri['guild_name']
embedded_mestieri = [(mestiere, model.encode(mestiere)) for mestiere in mestieri_name]
embedded_mestieri = list_to_dict(embedded_mestieri)

#see similarities
embedded_final = embedded_mestieri['SARTI']
for mestieri, embedding in embedded_mestieri.items():
    embed = embedding[0].reshape(1, -1)
    embedded_final = np.append(embedded_final, embed, axis = 0)
    

similarity = cosine_similarity(embedded_final)

positions = find_similarity(similarity, treshold = 0.8)

mestieri_simili = [(mestieri_name[value1 -1], mestieri_name[value2 - 1]) for value1, value2 in positions if value1 !=0 and value2 != 0]

low_skilled_occupation_definition = ['OPERAI',
 'AGRICOLTORI',
 'VITICOLTORI',
 'RIVENDITORI',
 'PASTORI',
 'CAPRAI',
 'CARRETTIERI',
 'BARCAIOLI',
 'MURATORI',
 'VENDITORI DI SECONDA MANO'
 'PESCATORI']
embedded_low_skill = [(mestiere, model.encode(mestiere)) for mestiere in low_skilled_occupation_definition]
embedded_low_skill = list_to_dict(embedded_low_skill)
embedded_final_low_skill =  embedded_low_skill['OPERAI']
for key, embedding in embedded_low_skill.items():
    embed = embedding[0].reshape(1, -1)
    embedded_final_low_skill = np.append(embedded_final_low_skill, embed, axis = 0)

for key, embedding in embedded_mestieri.items():
    embed = embedding[0].reshape(1, -1)
    embedded_final_low_skill = np.append(embedded_final_low_skill, embed, axis = 0)

similarity1 = cosine_similarity(embedded_final_low_skill)
positions1 = find_similarity(similarity1, treshold = 0.7)
positions1 = [value for value in positions1 if value[0] < 12 and value[1] >11]
low_skilled_guilds = [(mestieri_name[value[1] - 11]) for value in positions1]














