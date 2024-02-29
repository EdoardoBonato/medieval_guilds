<<<<<<< HEAD:python/final_population.py
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 12:32:25 2024

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
import re

path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merged_clean.xlsx"
merged = pd.read_excel(path)

grouped = merged.groupby(['place', 'guild_name'])
def low_high_values(x):
    return pd.Series([x.nsmallest(2).values, x.nlargest(2).values], index=['Lowest', 'Highest'])
grouped_percentile = grouped['combined_years'].apply(low_high_values)

def approximate_year(year):
    return round(year / 40) * 40

grouped_min = grouped.agg({'combined_years' : ['min', 'max']})
grouped_min[['group_min', 'group_max']] = grouped_min['combined_years'].apply(approximate_year)
grouped_min = grouped_min.reset_index()
grouped_min.columns = ['place', 'guild_name', 'min_year', 'max_year', 'group_min', 'group_max']
grouped_min = grouped_min.sort_values(by=['place', 'min_year'])
#create variable to have guild number
regrouped = grouped_min.groupby('place')
grouped_min['guilds_nr'] = regrouped.cumcount() + 1

#higher size data
#dataset_chat_gpt
path_pop_plus = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\italian_cities_population.xlsx"
pop_plus = pd.read_excel(path_pop_plus)
pop_plus = pop_plus.rename(columns = {'city' : 'place', 'inhabitants in 000-s' : 'population', 'year': 'group_min'})
pop_plus['place'] = pop_plus['place'].str.upper()
pop_plus['population'] = pop_plus['population'].apply(lambda x: x*1000)
common_cities_plus = []
for place in grouped_min['place']:
    for city in pop_plus['place']:
        if city == place:
            common_cities_plus.append(city)
            
common_cities_plus = set(common_cities_plus)
#merge the datasets
population_plus = pd.merge(grouped_min, pop_plus, on = ['place', 'group_min'], how = 'left')

#dataset parente
path_parente = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\datasetguilds.xls"

parente_population = pd.read_excel(path_parente)

parente_population['place'] = parente_population['place'].str.upper()
parente_population = parente_population.rename(columns = {'year': 'group_min'})
parente_population['pop'] = parente_population['pop']*1000
common_cities = list(set(grouped_min['place']).intersection(set(parente_population['place'])))    
print(len(set(parente_population['place'])))
#merge dataset
merged_population_parente = pd.merge(grouped_min, parente_population, on = ['place', 'group_min'], how ='left')

#merge the two high size datasets
common_columns = list(set(merged_population_parente.columns).intersection(set(population_plus.columns)))    
merged_population = pd.merge(population_plus, merged_population_parente, on = common_columns, how = 'left')

#smaller dataset(dataset_alfani)
path_population = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\Database_AlfaniAndPercoco20190308144130.xlsx"
population = pd.read_excel(path_population, header = 2)
population = population.drop(population.columns[[4, 5, 6, 7]], axis = 1)

common_cities = []
for place in grouped_min['place']:
    for city in population['place']:
        if city == place:
            common_cities.append(city)
            
common_cities = set(common_cities)

#merge with the datasets
guild_pop = pd.merge(merged_population, population, on = 'place', how = 'left')
numerical_values = re.findall(r'\d+\.\d+|\d+', str(guild_pop.columns))
numerical_values = [int(x) for x in numerical_values[2:]]
pop_columns = [column for column in guild_pop.columns if 'pop' in column and column!= 'population' and column!= 'pop']
columns_to_check = []
for index,row in guild_pop.iterrows():
    if row['group_min'] in numerical_values:
        column = 'pop' + str(int(row['group_min']))
        value = guild_pop.at[index, column]
        columns_to_check.append(column)
        for pop_column in pop_columns:
            guild_pop.at[index, pop_column] = np.nan
        guild_pop.at[index, column] = value

# Custom function to get the first non-NaN value from specified columns
def first_non_nan_in_columns(row):
    return next((value for col, value in row[columns_to_check].items() if not pd.isna(value)), np.nan)

# Create a new column based on the first non-NaN value in the specified columns
guild_pop['population_x'] = guild_pop.apply(first_non_nan_in_columns, axis=1)

#compare the value in population and population_x
mask = guild_pop['population'].notna() & guild_pop['population_x'].notna()

correspondence = guild_pop[mask]['population'] == guild_pop[mask]['population_x']
correspondence = pd.DataFrame(correspondence)
#70% do not match, let's try a looser definition
correspondence_loose = [(key, row['population'] - row['population_x']) for key, row in guild_pop[mask].iterrows()]
#still do not match, let's use parente's data where possible
guild_pop['population_final'] = np.where(guild_pop['population_x'].isna(), guild_pop['population'], guild_pop['population_x'])
guild_pop['population_final'] = np.where(guild_pop['population_final'].isna(), guild_pop['pop'], guild_pop['population_final'])

# Calculate the correlations for each unique value in 'Place'
correlations =  guild_pop.groupby('place').apply(lambda x: x['population_final'].corr(x['guilds_nr']))
correlations = correlations.dropna()
correlations.name = 'values'
average_corr = correlations.mean()

# Display the correlations(few data)
weights = frequencies(grouped_min['place'])
correlations = pd.concat([correlations, weights], axis = 1, join = 'inner')
average_weighted_corr = np.average(correlations['values'], weights= correlations['weights'])

#density of guilds on population
guild_pop['density_of_guilds'] = guild_pop['guilds_nr']/guild_pop['population_final'] * 10000
guild_pop.to_excel(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\population\population_final.xlsx')

differences = (guild_pop['population'] - guild_pop['pop'])/ guild_pop['pop']
average_diff = np.mean(differences)
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
         



=======
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 12:32:25 2024

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
import re

path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merged_clean.xlsx"
merged = pd.read_excel(path)

grouped = merged.groupby(['place', 'guild_name'])
def low_high_values(x):
    return pd.Series([x.nsmallest(2).values, x.nlargest(2).values], index=['Lowest', 'Highest'])
grouped_percentile = grouped['combined_years'].apply(low_high_values)

def approximate_year(year):
    return round(year / 40) * 40

grouped_min = grouped.agg({'combined_years' : ['min', 'max']})
grouped_min[['group_min', 'group_max']] = grouped_min['combined_years'].apply(approximate_year)
grouped_min = grouped_min.reset_index()
grouped_min.columns = ['place', 'guild_name', 'min_year', 'max_year', 'group_min', 'group_max']
grouped_min = grouped_min.sort_values(by=['place', 'min_year'])
#create variable to have guild number
regrouped = grouped_min.groupby('place')
grouped_min['guilds_nr'] = regrouped.cumcount() + 1

#higher size data
#dataset_chat_gpt
path_pop_plus = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\italian_cities_population.xlsx"
pop_plus = pd.read_excel(path_pop_plus)
pop_plus = pop_plus.rename(columns = {'city' : 'place', 'inhabitants in 000-s' : 'population', 'year': 'group_min'})
pop_plus['place'] = pop_plus['place'].str.upper()
pop_plus['population'] = pop_plus['population'].apply(lambda x: x*1000)
common_cities_plus = []
for place in grouped_min['place']:
    for city in pop_plus['place']:
        if city == place:
            common_cities_plus.append(city)
            
common_cities_plus = set(common_cities_plus)
#merge the datasets
population_plus = pd.merge(grouped_min, pop_plus, on = ['place', 'group_min'], how = 'left')

#dataset parente
path_parente = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\datasetguilds.xls"

parente_population = pd.read_excel(path_parente)

parente_population['place'] = parente_population['place'].str.upper()
parente_population = parente_population.rename(columns = {'year': 'group_min'})
parente_population['pop'] = parente_population['pop']*1000
common_cities = list(set(grouped_min['place']).intersection(set(parente_population['place'])))    
print(len(set(parente_population['place'])))
#merge dataset
merged_population_parente = pd.merge(grouped_min, parente_population, on = ['place', 'group_min'], how ='left')

#merge the two high size datasets
common_columns = list(set(merged_population_parente.columns).intersection(set(population_plus.columns)))    
merged_population = pd.merge(population_plus, merged_population_parente, on = common_columns, how = 'left')

#smaller dataset(dataset_alfani)
path_population = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\Database_AlfaniAndPercoco20190308144130.xlsx"
population = pd.read_excel(path_population, header = 2)
population = population.drop(population.columns[[4, 5, 6, 7]], axis = 1)

common_cities = []
for place in grouped_min['place']:
    for city in population['place']:
        if city == place:
            common_cities.append(city)
            
common_cities = set(common_cities)

#merge with the datasets
guild_pop = pd.merge(merged_population, population, on = 'place', how = 'left')
numerical_values = re.findall(r'\d+\.\d+|\d+', str(guild_pop.columns))
numerical_values = [int(x) for x in numerical_values[2:]]
pop_columns = [column for column in guild_pop.columns if 'pop' in column and column!= 'population' and column!= 'pop']
columns_to_check = []
for index,row in guild_pop.iterrows():
    if row['group_min'] in numerical_values:
        column = 'pop' + str(int(row['group_min']))
        value = guild_pop.at[index, column]
        columns_to_check.append(column)
        for pop_column in pop_columns:
            guild_pop.at[index, pop_column] = np.nan
        guild_pop.at[index, column] = value

# Custom function to get the first non-NaN value from specified columns
def first_non_nan_in_columns(row):
    return next((value for col, value in row[columns_to_check].items() if not pd.isna(value)), np.nan)

# Create a new column based on the first non-NaN value in the specified columns
guild_pop['population_x'] = guild_pop.apply(first_non_nan_in_columns, axis=1)

#compare the value in population and population_x
mask = guild_pop['population'].notna() & guild_pop['population_x'].notna()

correspondence = guild_pop[mask]['population'] == guild_pop[mask]['population_x']
correspondence = pd.DataFrame(correspondence)
#70% do not match, let's try a looser definition
correspondence_loose = [(key, row['population'] - row['population_x']) for key, row in guild_pop[mask].iterrows()]
#still do not match, let's use parente's data where possible
guild_pop['population_final'] = np.where(guild_pop['population_x'].isna(), guild_pop['population'], guild_pop['population_x'])
guild_pop['population_final'] = np.where(guild_pop['population_final'].isna(), guild_pop['pop'], guild_pop['population_final'])

# Calculate the correlations for each unique value in 'Place'
correlations =  guild_pop.groupby('place').apply(lambda x: x['population_final'].corr(x['guilds_nr']))
correlations = correlations.dropna()
correlations.name = 'values'
average_corr = correlations.mean()

# Display the correlations(few data)
weights = frequencies(grouped_min['place'])
correlations = pd.concat([correlations, weights], axis = 1, join = 'inner')
average_weighted_corr = np.average(correlations['values'], weights= correlations['weights'])

#density of guilds on population
guild_pop['density_of_guilds'] = guild_pop['guilds_nr']/guild_pop['population_final'] * 10000
guild_pop.to_excel(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\population\population_final.xlsx')

differences = (guild_pop['population'] - guild_pop['pop'])/ guild_pop['pop']
average_diff = np.mean(differences)
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
         



>>>>>>> 4cf4cb7af20a6864c515bfbc935e39f7634a9d44:final_population.py
