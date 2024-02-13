# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 11:30:20 2024

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
from text_analysis import find_similarity, compare_dict

path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merged_clean_w_regions1.xlsx"
merged = pd.read_excel(path)
def approximate(year):
    return round(year /40) * 40
mappa = {'Trentino-Alto Adige/Südtirol': 'Trentino'}
merged['region'] = merged['region'].replace(mappa)
merged['group'] = merged['combined_years'].apply(approximate)
grouped = merged.groupby(['region', 'guild_name'])
grouped_min = grouped.agg({'combined_years' : 'min'})
grouped_min['group'] = grouped_min['combined_years'].apply(approximate)
grouped_min = grouped_min.reset_index()
grouped_min.columns = ['region', 'guild_name','year', 'group']
grouped_min = grouped_min.sort_values(by=['region', 'year'])
#create variable to have guild number
regrouped = grouped_min.groupby('region')
grouped_min['guilds_nr'] = regrouped.cumcount() + 1
effective_trend_city = merged.groupby(['region', 'group'])['guild_name'].count() 
effective_trend_city = effective_trend_city.reset_index()
effective_trend_city.columns = ['region', 'group', 'region_new_guilds']
merged = pd.merge(merged, effective_trend_city, on = ['region', 'group'], how = 'left')
merged = merged.groupby(['region','group']).agg({'combined_years': 'min', 'region_new_guilds' : 'max'})
merged = merged.reset_index()
merged['combined_years'] = merged['combined_years'].astype(int)
merged = merged.sort_values(by = ['region', 'combined_years'])
merged = merged.rename(columns = {'combined_years' : 'year'})
grouped_min.to_excel(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\duration\region_trend_total.xlsx')
merged.to_excel(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\duration\region_trend.xlsx')