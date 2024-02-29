
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
merged = pd.read_excel(path)

# Set the display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

grouped = merged.groupby(['place', 'guild_name'])
grouped_min = grouped.agg({'combined_years' : 'min', 'unskilled' : 'first'})
grouped_min = grouped_min.sort_values(by = 'combined_years')
# Reset the index
grouped_min.reset_index(inplace=True)

# calculate the total number of guilds
grouped_min['total_nr'] = grouped_min.index

#total number of unskilled guilds
grouped_min['unskilled_nr'] = grouped_min['unskilled'].cumsum()
#percentage on total guilds
grouped_min['unskilled_perc'] = grouped_min['unskilled_nr'] / grouped_min['total_nr']*100

#nr og guilds by year(group)
grouped_min = grouped_min.reset_index()

def approximate_year(year):
    return round(year / 40) * 40
grouped_min['group'] = grouped_min['combined_years'].apply(approximate_year)
grouped_min = grouped_min.sort_values(by=['place', 'combined_years'])
grouped_years = grouped_min.groupby('group')
grouped_place = grouped_min.groupby('place')
grouped_min['guilds_nr_city'] = grouped_place.cumcount() + 1

#number of unskilled guilds in cities
grouped_min['unskilled_nr_city'] = grouped_place['unskilled'].cumsum()
#percentage on total guilds in cities
grouped_min['unskilled_perc_city'] = grouped_min['unskilled_nr_city'] / grouped_min['guilds_nr_city']*100
grouped_min.to_excel(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\grouped_min.xlsx')
listaa = grouped_min['combined_years'].apply(lambda x: type(x) is not int)
