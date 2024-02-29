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
import random

path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merged_w_abolition.xlsx"    
merged = pd.read_excel(path)
merged = merged[(merged.change == 'IS ABOLISHED') | (merged['change'].isna())]
merged = merged[merged['combined_years'] != 0]
grouped = merged.groupby(['place', 'guild_name'])
grouped_min_max = grouped.agg({'combined_years' : ['min', 'max'], 'unskilled' : 'first'})
def approximate_year(year):
    return round(year / 50) * 50
grouped_min_max[['group_min', 'group_max']] = grouped_min_max['combined_years'].apply(approximate_year)
grouped_min_max = grouped_min_max.reset_index()
grouped_min_max.columns = ['place', 'guild_name', 'min_year', 'max_year', 'first', 'group_min', 'group_max']

#calculate average duration
grouped_min_max['duration'] = grouped_min_max['max_year'] - grouped_min_max['min_year']
calculate_duration = grouped_min_max[grouped_min_max.duration > 20]
average_duration = np.mean(calculate_duration['duration'])

grouped_min_max = grouped_min_max.sort_values(by = 'duration', ascending = False)   
grouped_min_max.to_excel(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\grouped_min_max.xlsx')
