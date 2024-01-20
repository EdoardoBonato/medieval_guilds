# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 13:06:35 2023

@author: edobo
"""

import pandas as pd
import numpy as np
import xlsxwriter
import json
import re

p_mocarelli = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Mocarelli\db_mocarelli.xlsx"
mocarelli = pd.read_excel(p_mocarelli, sheet_name = 'Data_w_region',header = 0)
p_population = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\Database_AlfaniAndPercoco20190308144130.xlsx"
population = pd.read_excel(p_population, header = 2)

population = population.drop(population.columns[[4, 5, 6, 7]], axis = 1)
#create variable to have guild number
group_by_place = mocarelli.groupby('Place')
mocarelli['guilds_nr'] = group_by_place.cumcount() +1 

common_cities = []
for place in mocarelli['Place']:
    for city in population['Place']:
        if city == place:
            common_cities.append(city)
            
common_cities = set(common_cities)


guild_pop = pd.merge(mocarelli, population, on = 'Place', how = 'inner')

numerical_values = re.findall(r'\d+\.\d+|\d+', str(guild_pop.columns))
numerical_values = [int(x) for x in numerical_values[3:]]
pop_columns = [column for column in guild_pop.columns if 'pop' in column]
columns_to_check = []
for index,row in guild_pop.iterrows():
    if row['Group'] in numerical_values:
        column = 'pop' + str(row['Group'])
        value = guild_pop.at[index, column]
        columns_to_check.append(column)
        for pop_column in pop_columns:
            guild_pop.at[index, pop_column] = np.nan
        guild_pop.at[index, column] = value
    else :
        guild_pop = guild_pop.drop(index)
        


# Custom function to get the first non-NaN value from specified columns
def first_non_nan_in_columns(row):
    return next((value for col, value in row[columns_to_check].items() if not pd.isna(value)), np.nan)

# Create a new column based on the first non-NaN value in the specified columns
guild_pop['population'] = guild_pop.apply(first_non_nan_in_columns, axis=1)

# Calculate the correlations for each unique value in 'Place'
correlations =  guild_pop.groupby('Place').apply(lambda x: x['population'].corr(x['guilds_nr']))
correlations.name = 'values'
average_corr = correlations.mean()
# Display the correlations
weights = pd.read_excel(p_mocarelli, sheet_name = 'weights')
weights.set_index('Place', inplace = True)
correlation_weights = weights['weights']
correlation_weights = correlation_weights.dropna()
correlations = correlations.dropna()
correlations = pd.concat([correlations, correlation_weights], axis = 1, join = 'inner')
average_weighted_corr = np.average(correlations['values'], weights= correlations['weights'])

writer = pd.ExcelWriter(p_mocarelli, engine = 'openpyxl', mode = 'a')
guild_pop.to_excel(writer, sheet_name = 'population')
writer.close()