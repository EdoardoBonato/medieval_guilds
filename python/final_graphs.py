# -*- coding: utf-8 -*-

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

path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\duration\guilds_number2_region.xlsx"
#path_population = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\population\population_final.xlsx"
merged = pd.read_excel(path)
fig4 = go.Figure()

def graph_creation_plural(cities=[]):
    
    colors = [
        'red', 'green', 'blue', 'purple', 'orange', 
        'yellow',  'olive',
    ]
    
    fig = go.Figure()
    for city in cities:
        if city in cities_evolution:
            # Make sure each city gets a unique color
            color = colors[cities.index(city) % len(colors)]
            serie = cities_evolution[city]
            x_values = serie.index.tolist()
            y_values = serie['guilds_nr_place'].tolist()

            fig.add_trace(go.Scatter(
                x=x_values,
                y=y_values,
                line_color=color,
                name=city
            ))

    # Update the layout
    fig.update_layout(
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
        )
    )

    # Save the figure to an HTML file
    fig.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts\cumulative.html')



def place_evolution(city = None):
    name = merged[merged.place == city]
    name_year = name.groupby('year')
    name_evolution = name_year.agg({'guilds_nr_place': 'max'})
    
    return name_evolution

cities_evolution = {}
for city in merged['place'].unique():
    cities_evolution[city] = place_evolution(city)

cities_ = ['ROMA', 'VENEZIA', 'GENOVA', 'MILANO', 'BOLOGNA', 'NAPOLI', 'FIRENZE']
graph_creation_plural(cities_)
    
merged = merged.sort_values('year')
merged['log_guilds'] = np.log(merged['total_guilds_number'])
mask = merged['exist'] == 1
mask_n = merged['exist'] == -1
ceased_guilds = merged[mask_n].groupby('group').agg({'exist' : 'sum'})
ceased_guilds = ceased_guilds.reset_index()
ceased_guilds.columns = ['group', 'ceased_guilds']
new_guilds = merged[mask].groupby('group').agg({'exist' : 'sum'})
new_guilds = new_guilds.reset_index()
new_guilds.columns = ['group', 'new_guilds']
merged = pd.merge(merged, new_guilds, on = 'group', how = 'left')
merged = pd.merge(merged, ceased_guilds, on = 'group', how = 'left')
merged['ceased_guilds'] = merged['ceased_guilds'].fillna(0)
merged['new_guilds'] = merged['new_guilds'].fillna(0)
merged['ceased_guilds'] = merged['ceased_guilds'].abs()
#population = pd.read_excel(path_population)
number_of_guilds = merged[['group', 'year', 'place', 'total_guilds_number','net_new_guilds', 'new_guilds',
                           'ceased_guilds']]
number_of_guilds = number_of_guilds.sort_values('year')
number_of_guilds = number_of_guilds.reset_index()

matte_red = 'rgb(178, 34, 34)'  # A darker, less saturated red
matte_blue = 'rgb(70, 130, 180)'  # A darker, less saturated blue
matte_orange = 'rgb(255, 140, 0)'  # A darker, less saturated orange
fig1 = go.Figure()

fig1.add_trace(go.Scatter(
    x = number_of_guilds['year'],
    y = number_of_guilds['total_guilds_number'],
    line_color= matte_blue,
    name = 'total guilds'
    ))

fig1.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    title={
    'text': "",  # Set the title text here
    'y':0.9,
    'x':0.5,
    'xanchor': 'center',
    'yanchor': 'top'
    },
    xaxis = dict(
        range = [1100, 1825],
        showgrid = False,
        title = 'year',
        tickmode = 'linear',
        tick0 = 1100,
        dtick = 25
    ),
    yaxis = dict(
        #range = (-10, 10),
        title = 'total number of guilds',
        showgrid = True,
        zeroline = True,
        zerolinecolor = 'grey',
        gridcolor = 'rgb(190, 190, 190)',
        griddash = 'dash'
    ),
    yaxis2 = dict(
        showgrid = False,
        title = 'guilds number',
        #range= (-60, 60),
        zeroline = True,
        zerolinecolor = 'grey',
        gridcolor = 'rgb(211, 211, 211)',
        griddash = 'dash'
    ),
)


fig1.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts\total_guilds.html')


fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x = number_of_guilds['group'],
    y = number_of_guilds['net_new_guilds'],
    line_color= matte_blue,
    name = 'new guilds'
    ))

fig2.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    title={
    'text': "",  # Set the title text here
    'y':0.9,
    'x':0.5,
    'xanchor': 'center',
    'yanchor': 'top'
    },
    xaxis = dict(
        range = [1100, 1775],
        showgrid = False,
        title = 'year',
        tickmode = 'linear',
        tick0 = 1100,
        dtick = 25
    ),
    yaxis = dict(
        range = [-150, 150],
        title = 'new net guilds',
        showgrid = True,
        zeroline = True,
        zerolinecolor = 'grey',
        gridcolor = 'rgb(190, 190, 190)',
        griddash = 'dash'
    ),
    yaxis2 = dict(
        showgrid = False,
        title = 'guilds number',
        #range= (-60, 60),
        zeroline = True,
        zerolinecolor = 'grey',
        gridcolor = 'rgb(211, 211, 211)',
        griddash = 'dash'
    ),
)


fig2.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts\new_net_guilds.html')


fig3 = go.Figure()

fig3.add_trace(go.Scatter(
    x = number_of_guilds['group'],
    y = number_of_guilds['new_guilds'],
    line_color= matte_blue,
    name = 'new guilds'
    ))

fig3.add_trace(go.Scatter(
    x = number_of_guilds['group'],
    y = number_of_guilds['ceased_guilds'],
    line_color= matte_red,
    name = 'extinguished guilds'
    ))

fig3.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    title={
    'text': "",  # Set the title text here
    'y':0.9,
    'x':0.5,
    'xanchor': 'center',
    'yanchor': 'top'
    },
    xaxis = dict(
        range = [1100, 1900],
        showgrid = False,
        title = 'year',
        tickmode = 'linear',
        tick0 = 1100,
        dtick = 25
    ),
    yaxis = dict(
        #range = (-10, 10),
        title = 'number of guilds',
        showgrid = True,
        zeroline = True,
        zerolinecolor = 'grey',
        gridcolor = 'rgb(190, 190, 190)',
        griddash = 'dash'
    ),
    yaxis2 = dict(
        showgrid = False,
        title = 'guilds number',
        #range= (-60, 60),
        zeroline = True,
        zerolinecolor = 'grey',
        gridcolor = 'rgb(211, 211, 211)',
        griddash = 'dash'
    ),
)


fig3.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts\new_and_destroyed.html')




def graph_creation(city, serie):
    fig5 = go.Figure()

    fig5.add_trace(go.Scatter(
        x = list(serie.index),
        y = list(serie.values),
        line_color='rgb(0,100,80)',
        name = str(city)
        ))
    fig5.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts' + '\\' + city + '.html')

for key,value in cities_evolution.items():
    do = graph_creation(key, cities_evolution[key])

    

#graph_creation_plural_pop(cities_)
'''
cities_pop_evolution = {}
for city in population['place'].unique():
    cities_pop_evolution[city] = place_pop_evolution(city)
def list_to_int(lst):
    return lst[0] if len(lst) == 1 else None

# Apply the function to each Series in the cities_pop_evolution dictionary
for city in cities_pop_evolution:
    cities_pop_evolution[city] = cities_pop_evolution[city].apply(list_to_int)
    

def place_pop_evolution(city = None):
    name = population[population.place == city]
    name_year = name.groupby('min_year')
    name_evolution = name_year['density_of_guilds'].apply(list)
 
    return name_evolution

'''














'''

=======
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

c
    
graph_creation_plural(cities_)

graph_creation_plural_pop(cities_)


'''







