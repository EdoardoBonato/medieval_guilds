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

path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merged_clean.xlsx" 
path_abolished = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\mocarelli_changes.xlsx"
merged = pd.read_excel(path)
abolished = pd.read_excel(path_abolished)
#adjust
abolished = abolished.rename(columns = {'Change' : 'change', 'Year' : 'combined_years'})
abolished['change'] = abolished['change'].str.upper()
changes_fr = frequencies(abolished['change'])

#add abolition years 
#we want tosimply add them as new rows
merged_w_abolished = pd.concat([merged, abolished])
#create a dictionary to associate GuildsID to name, place
place_name = [ (row['GuildsID'], (row['place'], row['guild_name'])) for index, row in merged.iterrows()]
id_dict = list_to_dict(place_name)
id_dict = {key: list(set(value)) for key, value in id_dict.items() if len(value) > 0}
id_dict = {key : value[0] for key, value in id_dict.items()}
#apply the associated names
merged_w_abolished['temp'] = merged_w_abolished['GuildsID'].map(id_dict)
merged_w_abolished['ciao'] = merged_w_abolished['temp'].apply(lambda x : x[0] if isinstance(x, tuple) else np.nan)
merged_w_abolished['wow'] = merged_w_abolished['temp'].apply(lambda x : x[1] if isinstance(x, tuple) else np.nan)
#substitute where we have the abolition years
mask = pd.isna(merged_w_abolished['place']) & pd.isna(merged_w_abolished['guild_name'])
merged_w_abolished.loc[mask, 'place'] = merged_w_abolished.loc[mask, 'ciao']
merged_w_abolished.loc[mask, 'guild_name'] = merged_w_abolished.loc[mask, 'wow']
merged_w_abolished = merged_w_abolished.drop(columns = ['ciao', 'wow', 'temp'])
changes_merged_fr = frequencies(merged_w_abolished['change'])
#export to excel
merged_w_abolished.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merged_w_abolition1.xlsx")