# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 21:53:43 2024

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

path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merged_clean.xlsx"
path_population = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\population\population_final.xlsx"
merged = pd.read_excel(path)
population = pd.read_excel(path_population)

grouped = merged.groupby(['place', 'guild_name'])

grouped_min = grouped.agg({'combined_years' : 'min'})

#nr og guilds by year(group)
grouped_min = grouped_min.reset_index()

def approximate_year(year):
    return round(year / 40) * 40
grouped_min['group'] = grouped_min['combined_years'].apply(approximate_year)
grouped_min = grouped_min.sort_values(by=['place', 'combined_years'])
grouped_years = grouped_min.groupby('group')
grouped_place = grouped_min.groupby('place')
number_of_guilds = grouped_years[['guild_name']].count()
#frequencies
cities = frequencies(grouped_min['place'])
#graph the overall trend of guilds
number_of_guilds = number_of_guilds.reset_index()

fig1 = go.Figure()

fig1.add_trace(go.Scatter(
    x = number_of_guilds['group'],
    y = number_of_guilds['guild_name'],
    line_color='rgb(0,100,80)',
    name = 'total'
    ))
fig1.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts\total_trend_nonet.html')

#define functions
def place_evolution(city = None):
    name = grouped_min[grouped_min.place == city]
    name_year = name.groupby('group')
    name_evolution = name_year['guild_name'].count()
    
    return name_evolution

def place_pop_evolution(city = None):
    name = population[population.place == city]
    name_year = name.groupby('min_year')
    name_evolution = name_year['density_of_guilds'].apply(list)
 
    return name_evolution

def graph_creation(city, serie):
    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(
        x = list(serie.index),
        y = list(serie.values),
        line_color='rgb(0,100,80)',
        name = str(city)
        ))
    fig1.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts' + '\\' + city + '.html')
   
def graph_creation_plural(cities = []):
    
    colors = [
        'red', 'green', 'blue', 'purple', 'orange', 
        'yellow', 'brown', 'pink', 'gray', 'olive',
        'azure', 'darkorange'
    ]
    
    fig1 = go.Figure()
    for city in cities:
        color = random.choice(colors)
        serie = cities_evolution[city]
        fig1.add_trace(go.Scatter(
            x = list(serie.index),
            y = list(serie.values),
            line_color= color,
            name = str(city)
            ))
       
    fig1.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts\cumulative.html')

def graph_creation_plural_pop(cities = []):
    
    colors = [
        'red', 'green', 'blue', 'purple', 'orange', 
        'yellow', 'brown', 'pink', 'gray', 'olive',
        'azure', 'darkorange'
    ]
    
    fig1 = go.Figure()
    for city in cities:
        color = random.choice(colors)
        serie = cities_pop_evolution[city]
        fig1.add_trace(go.Scatter(
            x = list(serie.index),
            y = list(serie.values),
            line_color= color,
            name = str(city)
            ))
       
    fig1.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts\cumulative_pop.html')

cities_pop_evolution = {}
for city in population['place'].unique():
    cities_pop_evolution[city] = place_pop_evolution(city)
def list_to_int(lst):
    return lst[0] if len(lst) == 1 else None

# Apply the function to each Series in the cities_pop_evolution dictionary
for city in cities_pop_evolution:
    cities_pop_evolution[city] = cities_pop_evolution[city].apply(list_to_int)

cities_evolution = {}
for city in grouped_min['place'].unique():
    cities_evolution[city] = place_evolution(city)
    
for key,value in cities_evolution.items():
    do = graph_creation(key, cities_evolution[key])
    
cities_ = [key for key,value in cities_evolution.items() if len(value) > 12 ] 

cities_ = ['ROMA', 'VENEZIA', 'GENOVA', 'MILANO', 'SAVONA', 'PIACENZA', 'BOLOGNA', 'PADOVA' , 'NAPOLI', 'FIRENZE']
    
graph_creation_plural(cities_)

graph_creation_plural_pop(cities_)














