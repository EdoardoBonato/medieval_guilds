# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 15:08:04 2024

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

#other set of graphs
path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\duration\guilds_number2.xlsx"
merged = pd.read_excel(path)
