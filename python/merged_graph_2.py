# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 01:02:41 2024

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

#other set of graphs
path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\duration\guilds_number2_region.xlsx"
path1 = r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\population\population_final1.xlsx'
path2 = r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\duration\region_trend.xlsx'
path3 = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\duration\region_trend_total.xlsx"
population = pd.read_excel(path1)
merged = pd.read_excel(path)
merged_region = pd.read_excel(path2)
merged_region_total = pd.read_excel(path3)
#create the set
bologna = merged[merged.place == 'BOLOGNA']
bologna_evolution = bologna[['year', 'total_guilds_number']]
bologna_evolution = bologna_evolution.set_index('year')
bologna_evolution = pd.Series(bologna_evolution['total_guilds_number'])

#data on new guilds
merged_trend = merged[['year', 'group', 'net_new_guilds']]
merged_trend = merged_trend.sort_values('year')
merged_trend = merged_trend.set_index('group')
merged_trend = pd.Series(merged_trend['net_new_guilds'])
threshold = -100
merged_trend
#data on total guilds
merged_total = merged[['year', 'group', 'total_guilds_number']]
merged_total = merged_total.sort_values('year')
merged_total = merged_total.groupby('year')['total_guilds_number'].max()
# Truncate values above the threshold
merged_trend = merged_trend[merged_trend >= threshold]
fig1 = go.Figure()

#new_guilds_series

fig1.add_trace(go.Scatter(
    x = list(merged_trend.index),
    y = list(merged_trend.values),
    line_color='rgb(0,100,80)',
    name = 'italy'
    ))

fig1.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts\net_new_guilds.html')
#net new_guild
fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x = list(merged_trend.index),
    y = list(merged_trend.values),
    line_color='rgb(0,100,80)',
    name = 'italy'
    ))
fig3.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts\net_new_guilds.html')
#total_guild_serie
fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x = list(merged_total.index),
    y = list(merged_total.values),
    line_color='rgb(0,100,80)',
    name = 'italy'
    ))
fig2.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts\total_guilds.html')

def graph_creation(city, serie):
    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(
        x = list(serie.index),
        y = list(serie.values),
        line_color='rgb(0,100,80)',
        name = str(city)
        ))
    fig1.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts'+ '\\' + city + '.html')

def place_evolution(city = None):
    
    name = merged[merged.place == city]
    name_evolution = name[['year', 'guilds_nr_place']]
    name_evolution = name_evolution.set_index('year')
    name_evolution = pd.Series(name_evolution['guilds_nr_place'])
    return name_evolution

def place_evolution_new(city = None):
    name = merged[merged.place == city]
    name_evolution = name[['year', 'city_net_new_guilds']]
    name_evolution = name_evolution.set_index('year')
    name_evolution = pd.Series(name_evolution['city_new_guilds'])
    return name_evolution

def region_evolution(regione = None):
    name = merged_region[merged_region.region == regione]
    name_evolution = name[['group', 'region_new_guilds']]
    name_evolution = name_evolution.set_index('group')
    name_evolution = pd.Series(name_evolution['region_new_guilds'])
    return name_evolution

def region_evolution_total(regione = None):
    name = merged_region_total[merged_region_total.region == regione]
    name_evolution = name[['year', 'guilds_nr']]
    name_evolution = name_evolution.set_index('year')
    name_evolution = pd.Series(name_evolution['guilds_nr'])
    return name_evolution
def graph_creation_plural(cities = [], dictionary = {}, name = None):
    
    colors = [
        'green', 'red',  'orange', 'blue', 'yellow', 
        'olive', 'brown', 'gray', 'olive',
        'azure', 'darkorange', 'black'
    ]
    
    fig1 = go.Figure()
    for n, city in enumerate(cities):
        color = colors[n]
        serie = dictionary[city]
        fig1.add_trace(go.Scatter(
            x = list(serie.index),
            y = list(serie.values),
            line_color= color,
            mode = 'lines', 
            name = str(city)
            ))
    fig1.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            title='year',
            tickmode='linear',
            dtick=25,
            range = [1175, 1900],
            tickfont=dict(
                color='black'  # Setting the tick font color to black
            )
        ),
        yaxis=dict(
            title='number of guilds',
            showgrid=True,
            zeroline=True,
            zerolinecolor='grey',
            gridcolor='rgb(190, 190, 190)',
            griddash='dash',
            tickfont=dict(
                color='black'  # Setting the tick font color to black
            )
        ))
    fig1.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts\cumulative_' + name + '_total1.html')

def place_pop_evolution(city = None):
    name = population[population.place == city]
    name_year = name.groupby('group').agg({'city_density_of_guilds' : 'max'})
    name_year = pd.Series(name_year['city_density_of_guilds'])
    return name_year

cities_pop_evolution = {}
for city in population['place'].unique():
    cities_pop_evolution[city] = place_pop_evolution(city)

# Apply the function to each Series in the cities_pop_evolution dictionary

    
cities_evolution = {}
for city in merged['place'].unique():
    cities_evolution[city] = place_evolution(city)
for key,value in cities_evolution.items():
    do = graph_creation(key, cities_evolution[key])

regions_evolution = {}
for city in merged_region['region'].unique():
    regions_evolution[city] = region_evolution(city)
for key,value in regions_evolution.items():
    do = graph_creation(key, regions_evolution[key])

regions_evolution_total = {}
for city in merged_region_total['region'].unique():
    regions_evolution_total[city + '_total'] = region_evolution_total(city)
for key,value in regions_evolution_total.items():
    do = graph_creation(key, regions_evolution_total[key])
cities_ = ['VENEZIA', 'ROMA', 'BOLOGNA', 'GENOVA', 'MILANO', 'NAPOLI', 'FIRENZE']

citi = ['FIRENZE']
regions = ['Veneto', 'Toscana', 'Emilia-Romagna']
regions_nord = ['Lombardia','Piemonte', 'Liguria']
graph_creation_plural(cities_, cities_evolution, name = 'number')
graph_creation_plural(cities_, cities_pop_evolution, name = 'density')
graph_creation_plural(citi, cities_evolution, name = 'florence')

graph_creation_plural(regions, regions_evolution, name = 'nord-est_centro')
graph_creation_plural(regions_nord, regions_evolution, name = 'nord-ovest')

