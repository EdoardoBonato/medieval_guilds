# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 17:12:14 2024

@author: edobo
"""


import pandas as pd
import numpy as np
import xlsxwriter
import json
import numpy as np
import math
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import sys
sys.path.append(r"C:\Users\edobo\OneDrive\Desktop\Python\modules")
from data_structures import list_to_dict
from data_structures import merge_dict
from statistical_calculations import frequencies
import ast
import re

#import datasets and reorder column
ogilvie_path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\ogilvie_translation_advanced.xlsx"
ogilvie = pd.read_excel(ogilvie_path)
column_names = ogilvie.columns.to_list()
columns = column_names[0: 10] + column_names[199:201]
ogilvie = ogilvie[columns]

#preliminary analysis on OGILVIE structure
ogilvie_years_frequencies = frequencies(ogilvie['year'])
ogilvie_years = ogilvie['year'].unique()
ogilvie_years_integer = [year for year in ogilvie_years if isinstance(year, int)]
ogilvie_years_string = [year for year in ogilvie_years if isinstance(year, str)]
'''
#list of "problematic" values, that is to say non integer values
ogilvie_years_int_str = [re.findall(r'\d+\.\d+|\d+', str(string)) for string in ogilvie_years_string if re.findall(r'\d+\.\d+|\d+', str(string))]
ogilvie_years_int_str = [year for year in ogilvie_years_int_str if len(year[0]) > 2 ]
ogilvie_years_in_str = [year for year in ogilvie_years_int_str if len(year) > 1]
ogilvie_century = [year for year in ogilvie_years_int_str if len(year[0]) <= 2 ]
ogilvie_years_to_fix = [lst for lst in ogilvie_years_in_str if sum(len(string) for string in lst) <= 6]
ogilvie_years_fixed = [[years[0], str(int(years[0]) + int(years[1]))] for years in ogilvie_years_to_fix] 
'''
#fix problematic values
def modify_years(year):
    if isinstance(year, int):
        return year
    elif isinstance(year, str):
        ogilvie_years_int_str = re.findall(r'\d+\.\d+|\d+', str(year))
        if len(ogilvie_years_int_str) > 1:
            if len(ogilvie_years_int_str[0]) > 2:
                if sum(len(string) for string in ogilvie_years_int_str) <= 6:
                    if len(ogilvie_years_int_str[1]) == 1:
                        fixed  = [ogilvie_years_int_str[0], str(ogilvie_years_int_str[0])[:3] + str(ogilvie_years_int_str[1])]
                    if len(ogilvie_years_int_str[1]) == 2:
                        fixed  = [ogilvie_years_int_str[0], str(ogilvie_years_int_str[0])[:2] + str(ogilvie_years_int_str[1])]
                    return fixed
    return year
ogilvie['year'] = ogilvie['year'].apply(modify_years)


#ogilvie['year'] = ogilvie['year'].apply(lambda x : [int(x[0]), int(x[1])] if isinstance(x, list) else x)
#transform multiple value in a cell (1300-1800) in a list
ogilvie['year'] = ogilvie['year'].apply(lambda x : re.findall(r'\d+\.\d+|\d+', str(x)) if not isinstance(x, list) else x)
#get different values in a cell (1300-1800) in two rows
ogilvie = ogilvie.explode('year')
ogilvie['year'] = ogilvie['year'].apply(lambda x : int(x) if isinstance(x, int) else x)
ogilvie = ogilvie.dropna(subset=['year'])
#clean from centuries(for now)
ogilvie['year'] = ogilvie['year'].apply(lambda x : x if len(str(x)) > 2 else np.nan)
ogilvie = ogilvie.dropna(subset=['year'])
ogilvie['correspondence_moc'] = ogilvie['correspondence_moc'].apply(lambda x : 0 if math.isnan(x) else x)
to_merge  = frequencies(ogilvie['correspondence_moc'])
#call the italian names(which will merge with mocarelli) 'guild_name'
ogilvie = ogilvie.rename(columns = {'guild_name' : 'guild_name_eng'})
ogilvie['guild_name'] = ogilvie['translation_moc']
#get the number of guild,place ogilvie
grouped_ogilvie = ogilvie.groupby(['guild_name_eng', 'place'])

#mocarelli
mocarelli_path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merge_senato_mocarelli_ADJUSTED.xlsx"
mocarelli_senato = pd.read_excel(mocarelli_path)
year_columns = mocarelli_senato.columns[28:129]
mocarelli_senato = pd.melt(mocarelli_senato, id_vars= ['guild_name', 'place'], value_vars = year_columns, ignore_index=False)
mocarelli_senato = mocarelli_senato.dropna(subset = ['value'])
mocarelli_senato = mocarelli_senato.drop('variable', axis = 1)
mocarelli_senato = mocarelli_senato.rename(columns = {'value' : 'year'})
grouped_mocarelli = mocarelli_senato.groupby(['guild_name', 'place'])

#proceed to merge
merged = pd.merge(ogilvie, mocarelli_senato, on = ['place', 'guild_name'], how = 'outer')
merged['year_x'] = merged['year_x'].apply(lambda x : int(x) if not isinstance(x, float) else x)
grouped = merged.groupby(['guild_name', 'place'])
grouped_min_max = grouped.agg({'year_x' : ['min', 'max']})
duration = [(row[1] - row[0]) for key,row in grouped_min_max.iterrows() if (row[1]- row[0])>= 10 ] 
average_duration = sum(duration) / len(duration)

merged.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\final_merging_attempt.xlsx")