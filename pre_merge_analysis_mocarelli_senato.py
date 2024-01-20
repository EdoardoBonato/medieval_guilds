
"""
Created on Sun Nov 12 20:14:08 2023

@author: edobo
"""

import pandas as pd
import numpy as np
import xlsxwriter
import json
import sys
sys.path.append(r"C:\Users\edobo\OneDrive\Desktop\Python\modules")
from statistical_calculations import frequencies
from text_analysis import similar_matrix_df
from text_analysis import threshold_change_df
import numpy as np
import math
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2

merged = pd.read_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merge_senato_mocarelli.xlsx")

place = frequencies(merged['place'])
mestieri = frequencies(merged['guild_name'])

#similarities between guilds
similarity_guilds = similar_matrix_df(merged, columns = ['guild_name', 'place'])
similarity_guilds_9 = threshold_change_df(merged, similarity_guilds, threshold = 0.93)

#MANUAL ADJUSTMENT MADE, let's see if now it is fine
merged_adj = pd.read_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merge_senato_mocarelli_ADJUSTED.xlsx")
similarity_guilds_adj = similar_matrix_df(merged_adj, columns = ['guild_name', 'place'])
similarity_guilds_9_adj = threshold_change_df(merged_adj, similarity_guilds_adj, threshold = 0.93)