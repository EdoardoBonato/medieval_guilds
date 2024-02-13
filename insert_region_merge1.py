# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 23:52:24 2024

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

path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merged_clean1.xlsx"
merged = pd.read_excel(path)

path_regioni = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\Elenco-comuni-italiani.xls"
regioni = pd.read_excel(path_regioni)


regioni['Denominazione in italiano'] = regioni['Denominazione in italiano'].str.upper()
regioni = regioni.rename(columns = {'Denominazione in italiano' : 'place', 'Denominazione regione' : 'region',
                                    'Ripartizione geografica' : 'area'})
regioni = regioni[['place', 'region', 'area']]
merged = pd.merge(merged,regioni, on ='place', how = 'left')
column = merged.columns.to_list()
merged.to_excel(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merged_clean_w_regions1.xlsx')
