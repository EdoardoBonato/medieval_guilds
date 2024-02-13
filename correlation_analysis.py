# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 15:08:04 2024

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
path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\duration\guilds_number2_adj.xlsx"
merged = pd.read_excel(path)
merged = merged[['place', 'group', 'guilds_nr_place', 'city_net_new_guilds', 'city_new_guilds' ]]

#total number
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
def identify_columns(column, dataframe):
    counter = (dataframe[column].isna().sum() / len(dataframe[column]))
    return counter
nan = [(column, identify_columns(column, merged)) for column in merged.columns]
to_drop = [column for column, missing in nan if missing > 0.7]
merged = merged.drop(columns = to_drop)
merged.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\correlation\dataset_to_correlate.xlsx")

#calculate the correlation, in the different periods
#let check the correlation in the first period
merged.reset_index(inplace = True)
merged_1 = merged[(merged.group < 1481) & (merged.group > 1160)]
nan = [(column, identify_columns(column, merged_1)) for column in merged_1.columns]
to_drop = [column for column, missing in nan if missing > 0.7]
merged_1 = merged_1.drop(columns = to_drop)
merged_1.fillna(0, inplace = True)
merged_1.set_index('group', inplace = True)
cor_matrix = merged_1.corr()
cor_matrix.fillna(0, inplace = True)
plt.figure(figsize=(12,5))
dissimilarity = 1 - abs(cor_matrix)
Z = linkage(squareform(dissimilarity), 'complete')
dendrogram(Z, labels=merged_1.columns, orientation='top', 
           leaf_rotation=90)
threshold = 0.8
labels = fcluster(Z, threshold, criterion='distance')
labels_order = np.argsort(labels)

#cluster second period
merged_2 = merged[merged.group > 1481]
merged_2.set_index('group', inplace = True)
cor_matrix_1 = merged_2.corr()
cor_matrix_1.fillna(0, inplace = True)
dissimilarity_1 = 1 - abs(cor_matrix)
Y = linkage(squareform(dissimilarity_1), 'complete')
dendrogram(Y, labels=merged_2.columns, orientation='top', 
           leaf_rotation=90)
threshold = 0.8
labels = fcluster(Y, threshold, criterion='distance')
labels_order = np.argsort(labels)
# Build a new dataframe with the sorted columns
for idx, i in enumerate(merged_1.columns[labels_order]):
    if idx == 0:
        clustered = pd.DataFrame(merged[i])
    else:
        df_to_append = pd.DataFrame(merged[i])
        clustered = pd.concat([clustered, df_to_append], axis=1)
        
plt.figure(figsize=(15,10))
correlations = clustered.corr()
sns.heatmap(round(correlations,2), cmap='RdBu', annot=True, 
            annot_kws={"size": 7}, vmin=-1, vmax=1)

#use now the new guilds number
merged = pd.read_excel(path)
merged_new = merged[['place', 'group', 'city_new_guilds' ]]
cities_ = ['VENEZIA', 'ROMA', 'BOLOGNA', 'GENOVA', 'MILANO', 'NAPOLI', 'FIRENZE', 'PALERMO',
           'VERONA', 'PADOVA', 'SAVONA', 'TORINO', 'PIACENZA']
merged_new = merged_new[merged_new['place'].isin(cities_)]
merged_new = merged_new.groupby(['group', 'place']).agg({'city_new_guilds' : 'max'})
merged_new.reset_index(inplace = True)
collection = {}
for city in merged_new['place'].unique():
    collection[city] = merged_new[merged_new.place == city]
    collection[city] = collection[city].rename(columns = {'city_new_guilds' : city})
    collection[city] = collection[city].drop(columns = 'place')

merged_new = pd.DataFrame(merged_new['group'].unique(), columns = ['group'])

for key, dataframe in collection.items():
    merged_new = pd.merge(merged_new, dataframe, on = 'group', how = 'left')


#calculate the correlation, in the different periods
#let check the correlation in the first period
nan = [(column, identify_columns(column,merged_new)) for column in merged_new.columns]
to_drop = [column for column, missing in nan if missing > 0.6]

merged_new= merged_new[(merged_new.group < 1800) & (merged_new.group > 1159)]
merged_new = merged_new.fillna(0)
merged_new.set_index('group', inplace = True)
cor_matrix = merged_new.corr()
cor_matrix.fillna(1, inplace = True)
plt.figure(figsize=(12,5))
dissimilarity = 1 - abs(cor_matrix)
Z = linkage(squareform(dissimilarity), 'complete')
dendrogram(Z, labels=merged_new.columns, orientation='top', 
           leaf_rotation=90)
threshold = 0.3
labels = fcluster(Z, threshold, criterion='distance')
labels_order = np.argsort(labels)

for idx, i in enumerate(merged_new.columns[labels_order]):
    if idx == 0:
        clustered = pd.DataFrame(merged_new[i])
    else:
        df_to_append = pd.DataFrame(merged_new[i])
        clustered = pd.concat([clustered, df_to_append], axis=1)
        
plt.figure(figsize=(15,10))
correlations = clustered.corr()
sns.heatmap(round(correlations,2), cmap='RdBu', annot=True, 
            annot_kws={"size": 7}, vmin=-1, vmax=1)

