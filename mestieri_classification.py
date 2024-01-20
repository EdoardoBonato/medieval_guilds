# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 16:26:47 2024

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

#try to create a classification for low skilled guilds
low_skilled_occupation_definition = ['OPERAI',
 'AGRICOLTORI',
 'VITICOLTORI',
 'RIVENDITORI',
 'PASTORI',
 'BARCAIOLI',
 'MURATORI',
 'VENDITORI',
 'PESCATORI']
#embedd the low skill prototype
embedded_low_skill = [(mestiere, model.encode(mestiere)) for mestiere in low_skilled_occupation_definition]
embedded_low_skill = list_to_dict(embedded_low_skill)

lista = []
for key, embedding in embedded_mestieri.items():
    embed = embedding[0].reshape(1, -1)
    for key_low, embedding_low in embedded_low_skill.items():
        embed_low = embedding_low[0].reshape(1, -1)
        embedded = np.append(embed, embed_low, axis = 0)
        similarity = cosine_similarity(embedded)
        position = find_similarity(similarity, treshold = 0.67)
        if len(position) > 0 :
            lista.append((key, key_low))
            
def categorization(lista):
    for tupla in lista:
        if tupla[0] is in column:
            
            
#apply the changes
merged['category']

        
