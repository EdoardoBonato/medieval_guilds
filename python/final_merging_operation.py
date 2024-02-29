<<<<<<< HEAD:python/final_merging_operation.py

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

#preliminary analysis on OGILVIE structure
ogilvie_years_frequencies = frequencies(ogilvie['year'])
ogilvie_years = ogilvie['year'].unique()
ogilvie_years_integer = [year for year in ogilvie_years if isinstance(year, int)]
ogilvie_years_string = [year for year in ogilvie_years if isinstance(year, str)]

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

#call the italian names(which will merge with mocarelli) 'guild_name'
ogilvie = ogilvie.rename(columns = {'guild_name' : 'guild_name_eng'})
ogilvie['guild_name'] = ogilvie['translation_moc']
#attribute direct translation to the ogilvie only if there is not the mocarelli trasnlation
ogilvie['guild_name'] = np.where(ogilvie['guild_name'].isnull(), ogilvie['guild_name_ITA'], ogilvie['guild_name'])
#transform multiple value in a cell (1300-1800) in a list
ogilvie['year'] = ogilvie['year'].apply(lambda x : re.findall(r'\d+\.\d+|\d+', str(x)) if not isinstance(x, list) else x)
#get different values in a cell (1300-1800) in two rows
ogilvie = ogilvie.explode('year')
ogilvie['year'] = ogilvie['year'].apply(lambda x : int(x) if isinstance(x, int) else x)

ogilvie = ogilvie.dropna(subset=['year'])
#clean from centuries(for now)
ogilvie['year'] = ogilvie['year'].apply(lambda x : x if len(str(x)) > 2 else np.nan)
ogilvie = ogilvie.dropna(subset=['year'])
new_ogilvie_year_frequencies = frequencies(ogilvie['year'])
ogilvie['correspondence_moc'] = ogilvie['correspondence_moc'].apply(lambda x : 0 if math.isnan(x) else x)
to_merge  = frequencies(ogilvie['correspondence_moc'])

#get the number of guild,place ogilvie
grouped_ogilvie = ogilvie.groupby(['guild_name_eng', 'place'])
#calculate the average duration
ogilvie['year'] = ogilvie['year'].apply(lambda x : int(x) if not isinstance(x, float) else x)
grouped_ogilvie_min_max = grouped_ogilvie.agg({'year' : ['min', 'max']})
duration_ = [(row[1] - row[0]) for key,row in grouped_ogilvie_min_max.iterrows() if (row[1]- row[0])>= 10]
average_duration_ogilvie = sum(duration_) / len(duration_)

#mocarelli
mocarelli_path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merge_senato_mocarelli_ADJUSTED.xlsx"
mocarelli_senato = pd.read_excel(mocarelli_path)
mocarelli_senato_columns = mocarelli_senato.columns.to_list()
year_columns = mocarelli_senato_columns[29:131]
mocarelli_senato = pd.melt(mocarelli_senato, id_vars=
                           ['GuildsID', 'guild_name', 'place'], value_vars = year_columns, ignore_index=False)
mocarelli_senato = mocarelli_senato.dropna(subset = ['value'])
mocarelli_senato = mocarelli_senato.drop('variable', axis = 1)
mocarelli_senato = mocarelli_senato.rename(columns = {'value' : 'year'})
grouped_mocarelli = mocarelli_senato.groupby(['guild_name', 'place'])

#proceed to merge, without abolition
merged = pd.merge(ogilvie, mocarelli_senato, on = ['place', 'guild_name'], how = 'outer')
merged['year_x'] = merged['year_x'].apply(lambda x : int(x) if not isinstance(x, float) else x)
grouped = merged.groupby(['guild_name', 'place'])
anni = grouped[['year_x', 'year_y']].count()
grouped_anni = grouped.agg({'year_x': lambda x: list(x.dropna()), 'year_y': lambda y: list(y.dropna())})
merged['combined_years'] = merged.apply(lambda row: ','.join([str(year) for year in [row['year_x'], row['year_y']] if not pd.isnull(year)]), axis=1)
merged['combined_years'] = merged['combined_years'].apply(lambda x : x.split(','))
merged = merged.explode('combined_years')
merged['combined_years'] = merged['combined_years'].apply(lambda x : int(float(x)))
grouped = merged.groupby(['guild_name', 'place'])
anni_final = merged[['guild_name', 'place','combined_years']]
grouped_final = grouped.agg({'combined_years': lambda x: list(x.dropna())})
grouped_min_max = grouped.agg({'combined_years' : ['min', 'max']})
duration = [(row[1] - row[0]) for key,row in grouped_min_max.iterrows() if (row[1]- row[0])>= 10 ] 
average_duration = sum(duration) / len(duration)

#proceed to merge with abolition
path_abolishon = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\mocarelli_changes.xlsx"
abolished = pd.read_excel(path_abolishon)
abolished['Change'] = abolished['Change'].str.upper()
list_of_changes = abolished['Change'].unique()
abolished = abolished[abolished.Change == 'IS ABOLISHED']
merged_abolishon = pd.merge(merged, abolished, on = 'GuildsID', how = 'outer')
columns_abolished = merged_abolishon.columns.to_list()
reorder_columns_abolished = columns_abolished[7:13] + columns_abolished[206:213]
merged_abolishon = merged_abolishon[reorder_columns_abolished]
grouped_ab = merged_abolishon.groupby(['guild_name', 'place'])
grouped_anni_ab = grouped_ab.agg({'combined_years': lambda x: list(x.dropna()), 'Year': lambda y: list(y.dropna())})
merged_abolishon['combined_years'] = merged_abolishon.apply(lambda row: ','.join([str(year) for year in [row['combined_years'], row['Year']] if not pd.isnull(year)]), axis=1)
merged_abolishon['combined_years'] = merged_abolishon['combined_years'].apply(lambda x : x.split(','))
merged_abolishon = merged_abolishon.explode('combined_years')
merged_abolishon['combined_years'] = merged_abolishon['combined_years'].apply(lambda x : int(float(x)) if not isinstance(x, float) else x)
merged_abolishon_min_max = merged_abolishon.groupby(['guild_name', 'place']).agg({'combined_years' : ['min', 'max']})
duration = [(row[1] - row[0]) for key,row in merged_abolishon_min_max.iterrows() if (row[1]- row[0])>= 10 ] 
average_duration = sum(duration) / len(duration)

#order and export to excel
columns = merged.columns.to_list()
merged = merged.drop(columns = columns[0: 6])
columns = merged.columns.to_list()
reorder_columns = columns[0:3] + columns[4:7] + columns[200:202]+ [columns[203]] + [columns[202]] + [columns[3]]
merged = merged[reorder_columns]
merged.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\final_merging_attempt_raw.xlsx")
merged_abolishon_min_max.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\final_merging_attempt_w_abolished_raw.xlsx")
=======

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

#preliminary analysis on OGILVIE structure
ogilvie_years_frequencies = frequencies(ogilvie['year'])
ogilvie_years = ogilvie['year'].unique()
ogilvie_years_integer = [year for year in ogilvie_years if isinstance(year, int)]
ogilvie_years_string = [year for year in ogilvie_years if isinstance(year, str)]

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

#call the italian names(which will merge with mocarelli) 'guild_name'
ogilvie = ogilvie.rename(columns = {'guild_name' : 'guild_name_eng'})
ogilvie['guild_name'] = ogilvie['translation_moc']
#attribute direct translation to the ogilvie only if there is not the mocarelli trasnlation
ogilvie['guild_name'] = np.where(ogilvie['guild_name'].isnull(), ogilvie['guild_name_ITA'], ogilvie['guild_name'])
#transform multiple value in a cell (1300-1800) in a list
ogilvie['year'] = ogilvie['year'].apply(lambda x : re.findall(r'\d+\.\d+|\d+', str(x)) if not isinstance(x, list) else x)
#get different values in a cell (1300-1800) in two rows
ogilvie = ogilvie.explode('year')
ogilvie['year'] = ogilvie['year'].apply(lambda x : int(x) if isinstance(x, int) else x)

ogilvie = ogilvie.dropna(subset=['year'])
#clean from centuries(for now)
ogilvie['year'] = ogilvie['year'].apply(lambda x : x if len(str(x)) > 2 else np.nan)
ogilvie = ogilvie.dropna(subset=['year'])
new_ogilvie_year_frequencies = frequencies(ogilvie['year'])
ogilvie['correspondence_moc'] = ogilvie['correspondence_moc'].apply(lambda x : 0 if math.isnan(x) else x)
to_merge  = frequencies(ogilvie['correspondence_moc'])

#get the number of guild,place ogilvie
grouped_ogilvie = ogilvie.groupby(['guild_name_eng', 'place'])
#calculate the average duration
ogilvie['year'] = ogilvie['year'].apply(lambda x : int(x) if not isinstance(x, float) else x)
grouped_ogilvie_min_max = grouped_ogilvie.agg({'year' : ['min', 'max']})
duration_ = [(row[1] - row[0]) for key,row in grouped_ogilvie_min_max.iterrows() if (row[1]- row[0])>= 10]
average_duration_ogilvie = sum(duration_) / len(duration_)

#mocarelli
mocarelli_path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merge_senato_mocarelli_ADJUSTED.xlsx"
mocarelli_senato = pd.read_excel(mocarelli_path)
mocarelli_senato_columns = mocarelli_senato.columns.to_list()
year_columns = mocarelli_senato_columns[29:131]
mocarelli_senato = pd.melt(mocarelli_senato, id_vars=
                           ['GuildsID', 'guild_name', 'place'], value_vars = year_columns, ignore_index=False)
mocarelli_senato = mocarelli_senato.dropna(subset = ['value'])
mocarelli_senato = mocarelli_senato.drop('variable', axis = 1)
mocarelli_senato = mocarelli_senato.rename(columns = {'value' : 'year'})
grouped_mocarelli = mocarelli_senato.groupby(['guild_name', 'place'])

#proceed to merge, without abolition
merged = pd.merge(ogilvie, mocarelli_senato, on = ['place', 'guild_name'], how = 'outer')
merged['year_x'] = merged['year_x'].apply(lambda x : int(x) if not isinstance(x, float) else x)
grouped = merged.groupby(['guild_name', 'place'])
anni = grouped[['year_x', 'year_y']].count()
grouped_anni = grouped.agg({'year_x': lambda x: list(x.dropna()), 'year_y': lambda y: list(y.dropna())})
merged['combined_years'] = merged.apply(lambda row: ','.join([str(year) for year in [row['year_x'], row['year_y']] if not pd.isnull(year)]), axis=1)
merged['combined_years'] = merged['combined_years'].apply(lambda x : x.split(','))
merged = merged.explode('combined_years')
merged['combined_years'] = merged['combined_years'].apply(lambda x : int(float(x)))
grouped = merged.groupby(['guild_name', 'place'])
anni_final = merged[['guild_name', 'place','combined_years']]
grouped_final = grouped.agg({'combined_years': lambda x: list(x.dropna())})
grouped_min_max = grouped.agg({'combined_years' : ['min', 'max']})
duration = [(row[1] - row[0]) for key,row in grouped_min_max.iterrows() if (row[1]- row[0])>= 10 ] 
average_duration = sum(duration) / len(duration)

#proceed to merge with abolition
path_abolishon = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\mocarelli_changes.xlsx"
abolished = pd.read_excel(path_abolishon)
abolished['Change'] = abolished['Change'].str.upper()
list_of_changes = abolished['Change'].unique()
abolished = abolished[abolished.Change == 'IS ABOLISHED']
merged_abolishon = pd.merge(merged, abolished, on = 'GuildsID', how = 'outer')
columns_abolished = merged_abolishon.columns.to_list()
reorder_columns_abolished = columns_abolished[7:13] + columns_abolished[206:213]
merged_abolishon = merged_abolishon[reorder_columns_abolished]
grouped_ab = merged_abolishon.groupby(['guild_name', 'place'])
grouped_anni_ab = grouped_ab.agg({'combined_years': lambda x: list(x.dropna()), 'Year': lambda y: list(y.dropna())})
merged_abolishon['combined_years'] = merged_abolishon.apply(lambda row: ','.join([str(year) for year in [row['combined_years'], row['Year']] if not pd.isnull(year)]), axis=1)
merged_abolishon['combined_years'] = merged_abolishon['combined_years'].apply(lambda x : x.split(','))
merged_abolishon = merged_abolishon.explode('combined_years')
merged_abolishon['combined_years'] = merged_abolishon['combined_years'].apply(lambda x : int(float(x)) if not isinstance(x, float) else x)
merged_abolishon_min_max = merged_abolishon.groupby(['guild_name', 'place']).agg({'combined_years' : ['min', 'max']})
duration = [(row[1] - row[0]) for key,row in merged_abolishon_min_max.iterrows() if (row[1]- row[0])>= 10 ] 
average_duration = sum(duration) / len(duration)

#order and export to excel
columns = merged.columns.to_list()
merged = merged.drop(columns = columns[0: 6])
columns = merged.columns.to_list()
reorder_columns = columns[0:3] + columns[4:7] + columns[200:202]+ [columns[203]] + [columns[202]] + [columns[3]]
merged = merged[reorder_columns]
merged.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\final_merging_attempt_raw.xlsx")
merged_abolishon_min_max.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\final_merging_attempt_w_abolished_raw.xlsx")
>>>>>>> 4cf4cb7af20a6864c515bfbc935e39f7634a9d44:final_merging_operation.py
