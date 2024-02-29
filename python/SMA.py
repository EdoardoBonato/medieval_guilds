# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 19:57:08 2024

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
import seaborn as sns
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import squareform
import matplotlib.pyplot as plt
from data_structures import list_to_dict
from data_structures import merge_dict
from statistical_calculations import frequencies
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import random

#other set of graphs
path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\duration\guilds_number2.xlsx"
merged = pd.read_excel(path)
merged = merged[['place', 'group', 'guilds_nr_place' ]]
merged = merged.groupby(['group', 'place']).agg({'guilds_nr_place' : 'max'})
merged.reset_index(inplace = True)
collection = {}
for city in merged['place'].unique():
    collection[city] = merged[merged.place == city]
    collection[city] = collection[city].rename(columns = {'guilds_nr_place' : city})
    collection[city] = collection[city].drop(columns = 'place')

merged = pd.DataFrame(merged['group'].unique(), columns = ['group'])

for key, dataframe in collection.items():
    merged = pd.merge(merged, dataframe, on = 'group', how = 'left')
merged = merged.set_index('group')
merged.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\correlation\dataset_trends.xlsx")
merged_sma = pd.DataFrame()
for column in merged.columns:
    merged_sma[column] = merged[column].rolling(3).mean()

fig1 = go.Figure()

fig1.add_trace(go.Scatter(
    x = list(merged_sma.index),
    y = list(merged_sma['VENEZIA']),
    line_color='rgb(0,100,80)',
    name = 'italy'
    ))
fig1.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts\Venice.html')

def graph_creation_plural(cities = []):
    
    colors = [
        'red', 'green', 'blue', 'purple', 'orange', 
        'yellow', 'brown', 'gray', 'olive',
        'azure', 'darkorange', 'black'
    ]
    
    fig1 = go.Figure()
    for n, city in enumerate(cities):
        color = colors[n]
        fig1.add_trace(go.Scatter(
            x = list(merged_sma.index),
            y = list(merged_sma[city]),
            line_color= color,
            name = str(city)
            ))
       
    fig1.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts\cumulative_total_sma.html')
cities_ = ['ROMA', 'VENEZIA', 'GENOVA', 'MILANO', 'BOLOGNA' , 'NAPOLI', 'FIRENZE']
    
graph_creation_plural(cities_)