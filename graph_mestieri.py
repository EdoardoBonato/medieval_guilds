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

path = r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\grouped_min.xlsx'
merged = pd.read_excel(path)
grouppa = merged.sort_values(by=['combined_years'])  
grouppa = grouppa.groupby(['combined_years']).agg({'unskilled_perc':'mean'})
grouppa['unskilled_perc'] = grouppa['unskilled_perc'].apply(lambda x : x[0])
#create graphs regarding unskilled guilds
fig1 = go.Figure()

fig1.add_trace(go.Scatter(
        x = list(grouppa.index),
        y = list(grouppa['unskilled_perc']),
        line_color='rgb(0,100,80)',
        name = 'unskilled_perc'
        ))
       
fig1.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts\unskilled.html')