# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 17:44:22 2024

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
from plotly.subplots import make_subplots

path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\duration\guilds_number2_region.xlsx"
path_veneto = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_veneto_city.xlsx"
path_toscana = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_toscana.xlsx"
path_emilia = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\PIL-emilia.xlsx"
path_lazio = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_lazio.xlsx"
path_liguria = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_liguria.xlsx"
path_lombardia = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_lombardia.xlsx"
pil_piemonte = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_piemonte.xlsx"

merged = pd.read_excel(path)
pil_veneto = pd.read_excel(path_veneto)
pil_toscana = pd.read_excel(path_toscana)
#pil_emilia = pd.read_excel(path_emilia)
pil_lazio = pd.read_excel(path_lazio)
pil_liguria = pd.read_excel(path_liguria)
pil_lombardia = pd.read_excel(path_lombardia)
pil_piemonte = pd.read_excel(pil_piemonte)
def approximate(year):
    return round(year/10) * 10


pil_veneto['group'] = pil_veneto['year'].apply(approximate)
pil_toscana['group'] = pil_toscana['year'].apply(approximate)
#pil_emilia['group'] = pil_emilia['year'].apply(approximate)
pil_lazio['group'] = pil_lazio['year'].apply(approximate)
pil_liguria['group'] = pil_liguria['year'].apply(approximate)
pil_lombardia['group'] = pil_lombardia['year'].apply(approximate)
pil_piemonte['group'] = pil_piemonte['year'].apply(approximate)
def closest_year_value(group):
    closest_year = group['year'].sub(group.name - 1).abs().idxmin()
    return group.loc[closest_year, 'GDP']

def rolling_window_average(pil_region):
    pil_region.set_index('year', inplace=True)
    
    # Calculate rolling window average (window size: 11 years - 5 years before, the year itself, 5 years after)
    pil_region['rolling_avg_GDP'] = pil_region['GDP'].rolling(window=11, min_periods=1, center=True).mean()
    pil_region['rolling_avg_GDP_city'] = pil_region['GDP_city'].rolling(window=11, min_periods=1, center=True).mean()
    
    pil_region.reset_index(inplace=True)
    
    return pil_region


def data_extraction(dataset,  pil_region,regione = None,):
    veneto = merged[merged.region == regione]
    veneto = veneto[['group', 'region_new_guilds', 'guilds_nr_region']]
    veneto = veneto.groupby('group').agg({'region_new_guilds' : 'mean', 'guilds_nr_region' : 'max'})
    pil_region = rolling_window_average(pil_region)
    return veneto, pil_region



veneto, pil_veneto = data_extraction(merged, pil_veneto, 'Veneto')

merging_veneto = pd.merge(veneto, pil_veneto, left_on = 'group', right_on = 'year', how = 'inner')
merging_veneto['agg_change'] = merging_veneto['GDP'].pct_change()*100
merging_veneto['agg_change_city'] = merging_veneto['GDP_city'].pct_change()*100

#emilia, pil_emilia= data_extraction(merged,pil_emilia, 'Emilia-Romagna')
toscana, pil_toscana = data_extraction(merged,pil_toscana, 'Toscana')
lazio, pil_lazio = data_extraction(merged,pil_lazio,  'Lazio')
liguria, pil_liguria = data_extraction(merged, pil_liguria, 'Liguria')
lombardia, pil_lombardia = data_extraction(merged, pil_lombardia, 'Lombardia')
piemonte, pil_piemonte = data_extraction(merged, pil_piemonte, 'Piemonte')

regions = [(veneto,pil_veneto), (toscana, pil_toscana), (lazio, pil_lazio), (liguria, pil_liguria), (lombardia, pil_lombardia), (piemonte, pil_piemonte)]


def graph_creation(region, pil, name):
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(go.Scatter(
        x = list(pil['year']),
        y = list(pil['agg_change']),
        line_color='red',
        name = 'pil'),
        secondary_y = False,
        )
    fig1.add_trace(go.Scatter(
        x = list(region.index),
        y = list(region['region_new_guilds']),
        line_color='blue',
        name = 'guilds'),
        secondary_y = True
        )   
    fig1.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts\pil_' + name+ '.html')

graph_creation(veneto, pil_veneto, 'veneto')
fig1 = make_subplots(specs=[[{"secondary_y": True}]])
fig1.add_trace(go.Scatter(
    x = list(merging_veneto['year']),
    y = list(merging_veneto['agg_change']),
    line_color='red',
    name = 'pil'),
    secondary_y = False,
    )
fig1.add_trace(go.Scatter(
    x = list(merging_veneto['year']),
    y = list(merging_veneto['region_new_guilds']),
    line_color='blue',
    name = 'guilds'),
    secondary_y = True
    )   
fig1.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts\pil_veneto_city.html')

    
