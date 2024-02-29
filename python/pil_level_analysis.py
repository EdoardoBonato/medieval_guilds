# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 23:44:13 2024

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
path_pil = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_veneto_city.xlsx"
path_toscana = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_toscana_city.xlsx"
path_emilia = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_emilia_city.xlsx"
path_lazio = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_lazio_city.xlsx"
path_liguria = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_liguria_city.xlsx"
path_lombardia = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_lombardia_city.xlsx"
pil_piemonte = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_piemonte_city.xlsx"
pil_campania = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_campania_city.xlsx"
pil_sicilia = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_sicilia_city.xlsx"

merged = pd.read_excel(path)

pil_veneto = pd.read_excel(path_pil)
pil_toscana = pd.read_excel(path_toscana)
pil_emilia = pd.read_excel(path_emilia)
pil_lazio = pd.read_excel(path_lazio)
pil_liguria = pd.read_excel(path_liguria)
pil_lombardia = pd.read_excel(path_lombardia)
pil_piemonte = pd.read_excel(pil_piemonte)
pil_campania = pd.read_excel(pil_campania)
pil_sicilia = pd.read_excel(pil_sicilia)
def approximate(year):
    return round(year/10) * 10

def closest_year_value(group):
    closest_year = group['year'].sub(group.name - 1).abs().idxmin()
    return group.loc[closest_year, 'GDP']

def rolling_window_average(pil_region):
    pil_region.set_index('year', inplace=True)
    
    # Calculate rolling window average (window size: 11 years - 5 years before, the year itself, 5 years after)
    pil_region['rolling_avg_GDP'] = pil_region['GDP'].rolling(window=5, min_periods=1, center=True).mean()
    pil_region['rolling_avg_GDP_city'] = pil_region['GDP_city'].rolling(window = 5, min_periods = 1,
                                                                        center = True).mean()
    pil_region.reset_index(inplace=True)
    return pil_region


def data_extraction(dataset,  pil_region,regione = None,):
    veneto = merged[merged.region == regione]
    veneto = veneto[['group', 'region_new_guilds', 'guilds_nr_region', 'region_perc_new']]
    veneto = veneto.groupby('group').agg({'region_new_guilds' : 'mean', 'guilds_nr_region' : 'max', 
                                          'region_perc_new' : 'min'})
    pil_region = rolling_window_average(pil_region)
    return veneto, pil_region


veneto, pil_veneto = data_extraction(merged, pil_veneto, 'Veneto')
emilia, pil_emilia= data_extraction(merged,pil_emilia, 'Emilia-Romagna')
toscana, pil_toscana = data_extraction(merged,pil_toscana, 'Toscana')
lazio, pil_lazio = data_extraction(merged,pil_lazio,  'Lazio')
liguria, pil_liguria = data_extraction(merged, pil_liguria, 'Liguria')
lombardia, pil_lombardia = data_extraction(merged, pil_lombardia, 'Lombardia')
piemonte, pil_piemonte = data_extraction(merged, pil_piemonte, 'Piemonte')
campania, pil_campania = data_extraction(merged, pil_campania, 'Campania')
sicilia, pil_sicilia = data_extraction(merged, pil_sicilia, 'Sicilia')

pil_toscana['compunded'] = (pil_toscana['rolling_avg_GDP'] / pil_toscana['rolling_avg_GDP'].shift(25))**(1/25) - 1
pil_veneto['compunded'] = (pil_veneto['rolling_avg_GDP'] / pil_veneto['rolling_avg_GDP'].shift(25))**(1/25) - 1

def merging_function(region, pil):
    region = region.reset_index()
    all_years = pd.DataFrame({'group': range(1000, 1901, 10)})
    merged_df = pd.merge(all_years,region, on='group', how='left')
    merged_df['region_new_guilds'] = merged_df['region_new_guilds'].fillna(0)
    merging = pd.merge(merged_df, pil, left_on = 'group', right_on = 'year', how = 'inner')
    print(merging)
    merging = pd.merge(merged_df, merging, on = ['group', 'region_new_guilds', 'guilds_nr_region',
                                                              'region_perc_new'], how = 'outer')
    
    merging['agg_change'] = merging['rolling_avg_GDP'].pct_change()*100
    merging['agg_change_city'] = merging['rolling_avg_GDP_city'].pct_change()*100
    merging['log_return'] = np.log(merging['rolling_avg_GDP'] / merging['rolling_avg_GDP'].shift(1)) * 100
    merging['SMA'] = merging['agg_change'].rolling(window=3).mean()
    merging = merging.drop(merging.index[0])
    merging = merging[merging['group'] <= 1800]
    return merging

def merging_graph(region,pil):
    region = region.reset_index()
    merging = pd.merge(region, pil, left_on = 'group', right_on = 'year', how = 'left')
    merging['agg_change'] = merging['rolling_avg_GDP'].pct_change()*100
    merging = merging[merging['group']<= 1800]
    merging = merging[merging['group'] >= 1200]
    return merging

merging_veneto = merging_function(veneto, pil_veneto)
merging_toscana = merging_function(toscana, pil_toscana)
merging_lazio = merging_function(lazio, pil_lazio)
merging_liguria = merging_function(liguria, pil_liguria)
merging_lombardia = merging_function(lombardia, pil_lombardia)
merging_piemonte = merging_function(piemonte, pil_piemonte)
merging_campania = merging_function(campania, pil_campania)
merging_emilia = merging_function(emilia, pil_emilia)
merging_sicilia = merging_function(sicilia, pil_sicilia)


# Calculate the logarithmic return

merging_veneto['region'] = 'VENETO'
merging_toscana['region'] = 'TOSCANA'
merging_emilia['region'] = 'EMILIA'
merging_lazio['region'] = 'LAZIO'
merging_liguria['region'] = 'LIGURIA'
merging_lombardia['region'] = 'LOMBARDIA'
merging_piemonte['region'] = 'PIEMONTE'
merging_campania['region'] = 'CAMPANIA'
merging_sicilia['region'] = 'SICILIA'
#add all to a list
merged_df = [merging_veneto, merging_toscana, merging_lazio, merging_liguria, merging_lombardia, merging_piemonte, merging_campania, merging_emilia,
                merging_sicilia]
             

#calculate correlation
correlation_toscana = merging_toscana[['region_new_guilds', 'agg_change']].corr()
correlation = merging_veneto[['region_new_guilds', 'agg_change']].corr()
correlation_emilia =  merging_emilia[['region_new_guilds', 'agg_change']].corr()
correlation_lazio =  merging_lazio[['region_new_guilds', 'agg_change']].corr()
correlation_liguria =  merging_liguria[['region_new_guilds', 'agg_change']].corr()
correlation_lombardia = merging_lombardia[['region_new_guilds', 'agg_change']].corr()
correlation_piemonte = merging_piemonte[['region_new_guilds', 'agg_change']].corr()
correlation_campania = merging_campania[['region_new_guilds', 'agg_change']].corr()
correlation_sicilia = merging_sicilia[['region_new_guilds', 'agg_change']].corr()

total = pd.concat([merging_veneto, merging_toscana, merging_emilia, merging_campania, merging_liguria,
                   merging_lombardia, merging_piemonte, merging_sicilia, merging_lazio])
total.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\pil\pil_attempt_total_cities.xlsx")