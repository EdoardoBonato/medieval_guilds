# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 01:46:29 2024

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
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import random


path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\duration\guilds_number2.xlsx"
merged = pd.read_excel(path)
merged = merged[['place', 'group', 'guilds_nr_place' , 'total_guilds_number']]
merged['total_guilds_number'] = merged['guilds_nr_place']/ merged['total_guilds_number'] * 100
merged = merged.groupby(['group', 'place']).agg({'guilds_nr_place' : 'max', 'total_guilds_number' : 'max'})
merged.reset_index(inplace = True)
collection = {}
for city in merged['place'].unique():
    collection[city] = merged[merged.place == city]
    collection[city] = collection[city].rename(columns = {'guilds_nr_place' : city, 'total_guilds_number' : city + '_perc'})
    collection[city] = collection[city].drop(columns = 'place')

merged = pd.DataFrame(merged['group'].unique(), columns = ['group'])

for key, dataframe in collection.items():
    merged = pd.merge(merged, dataframe, on = 'group', how = 'left')

century = [1320, 1440, 1560, 1680, 1760, 1840]
rankings = {}
for cent in century:
    merged_1 = merged[merged.group <= cent]
    merged_1.set_index('group', inplace = True)
    ranking = [(merged_1.columns[i], merged_1.at[cent, merged_1.columns[i]], merged_1.at[cent, merged_1.columns[i+1]]) 
               for i in  range(0, len(merged_1.columns) - 1,2) if not pd.isna(merged_1.at[cent, merged_1.columns[i]])]
    ranking = sorted(ranking, key = lambda x : x[1], reverse = True)
    rankings[cent] = ranking

rankings = {key : value[0:10] for key, value in rankings.items()}

ranking_df = pd.DataFrame.from_dict(rankings)
ranking_df_1 = pd.DataFrame()
for column in ranking_df.columns:
    ranking_df[column] = ranking_df[column].astype(str)
    ranking_df_1[[column, str(column) + '_nr', str(column) + '_perc']] = ranking_df[column].str.split(',', expand = True)
    ranking_df_1[column] = ranking_df_1[column].str.replace('(', '').str.replace("'", "")
    ranking_df_1[str(column) + '_nr'] = ranking_df_1[str(column) + '_nr'].str.replace(')', '')
    ranking_df_1[str(column) + '_perc'] = ranking_df_1[str(column) + '_perc'].str.replace(')', '')
    ranking_df_1[str(column) + '_nr'] = ranking_df_1[str(column) + '_nr'].astype(float)
    ranking_df_1[str(column) + '_perc'] = ranking_df_1[str(column) + '_perc'].astype(float)
    
ranking_df_1.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\correlation\rankings.xlsx")

