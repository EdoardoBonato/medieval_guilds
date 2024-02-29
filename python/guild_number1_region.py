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
path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\duration\merged_duration_imputed2_region.xlsx"   
path_destination = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\duration\guilds_number2_region.xlsx"
merged = pd.read_excel(path)
def approximate(year):
   return ((year - 1) // 25 + 1) *25

#windsorize strange years
merged['max_year_or'] = merged['max_year']
merged['max_year'] = np.clip(merged['max_year'], None, 1880)

#now we want to obtain the total number of guilds
#let's create a new dummy variable, which takes 1 when guilds exists and 0 when it doesn't
#first explode the dataset
merged['min_year'] = merged['min_year'].astype(str)
merged['max_year'] = merged['max_year'].astype(str)
merged['year'] = list(zip(merged['min_year'], merged['max_year']))
merged = merged.explode('year')
#transform in int
merged['year'] = merged['year'].astype(float)
merged['year'] = merged['year'].round(0)
merged['group'] = merged['year'].apply(approximate)
#now we can create the dummy variable   
grouped = merged.groupby(['place', 'guild_name'])
max_years = grouped['year'].transform(max)
merged['exist']  = (merged['year'] != max_years).astype(int)
merged['exist'] = np.where(merged['exist']== 0, -1, merged['exist'])
#now we can calculate the total number of guilds existing in a period
merged_sorted = merged.sort_values('year')
merged_sorted['total_guilds_number'] = merged_sorted['exist'].cumsum() + 1
#now we can calculate the number of new born guilds
#net new born guilds
effective_trend = merged_sorted.groupby('year')['exist'].sum()
effective_trend_group = merged_sorted.groupby('group')['exist'].sum()
effective_trend_group = effective_trend_group.reset_index()
effective_trend_group.columns = ['group', 'net_new_guilds']
merged_sorted = pd.merge(merged_sorted, effective_trend_group, on = 'group' , how = 'left')

#now we can calculate the same data at place-level
#now we can group by place and sum the dummy variable
# First, sort the original DataFram
merged_sorted = merged_sorted.sort_values(['place', 'year'])
# Then calculate the cumulative sum within each 'place' group
merged_sorted['guilds_nr_place'] = merged_sorted.groupby('place')['exist'].cumsum()
effective_trend_city = merged_sorted.groupby(['place', 'group'])['exist'].sum() 
effective_trend_city = effective_trend_city.reset_index()
effective_trend_city.columns = ['place', 'group', 'city_net_new_guilds']
merged_sorted = pd.merge(merged_sorted, effective_trend_city, on = ['place', 'group'], how = 'left')
#now the new_guilds_non_net
non_net_trend_city = merged_sorted[merged_sorted['exist'] != -1]
non_net_trend_city = non_net_trend_city.groupby(['place', 'group'])['exist'].sum()
non_net_trend_city = non_net_trend_city.reset_index()
non_net_trend_city.columns = ['place', 'group', 'city_new_guilds']
#now the new net guilds by region
region_trend = merged_sorted.groupby(['region', 'group'])['exist'].sum()
region_trend = region_trend.reset_index()
region_trend.columns = ['region', 'group', 'region_new_guilds']

#percentage new guilds

#total number by region
merged_sorted = merged_sorted.sort_values(['region', 'year'])
merged_sorted['guilds_nr_region'] = merged_sorted.groupby('region')['exist'].cumsum()
merged_sorted = pd.merge(merged_sorted, non_net_trend_city, on = ['place', 'group'], how = 'left')
merged_sorted = pd.merge(merged_sorted, region_trend, on = ['region', 'group'], how = 'left')
merged_sorted['region_perc_new'] = merged_sorted['region_new_guilds']/ merged_sorted['guilds_nr_region']


merged_sorted.to_excel(path_destination)