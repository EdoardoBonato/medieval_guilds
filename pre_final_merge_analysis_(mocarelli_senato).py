
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
from text_analysis import similar_matrix_df, compare_dict,find_similarity
from data_structures import list_to_dict
import numpy as np
import math
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import collections
merged = pd.read_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merge_senato_mocarelli1.xlsx")
grouped1 = merged.groupby(['place', 'guild_name'])
model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v1')
place_name = [(row['place'], row['guild_name'])for key,row in merged.iterrows()]
place_name_dict = list_to_dict(place_name)
place_name_dict = {key : value for key, value in place_name_dict.items() if not len(value) == 0}
embedded_place_name = [(key,model.encode(valuex)) for key,value in place_name_dict.items() for valuex in value if isinstance(valuex, str)]
#embedded_place_name = [(key, valuex) for key, value in embedded_place_name.items() for valuex in value if isinstance(valuex, str)] = list_to_dict(ogilvie_new_names_dict)
embedded_dict = list_to_dict(embedded_place_name)

#similarities between guilds
embeddings = {}
for place, embedded_guilds in embedded_dict.items():
    guilds_place = embedded_guilds[0].reshape(1,-1)
    for guild in embedded_guilds:
        guild = guild.reshape(1, -1)
        guilds_place = np.append(guilds_place, guild, axis = 0)
    guilds_place = guilds_place[1:]
    embeddings[place] = guilds_place
similarities = {key : cosine_similarity(matrix) for key, matrix in embeddings.items()}
positions = [(key, find_similarity(matrix, treshold = 0.85)) for key, matrix in similarities.items()]
positions = [value for value in positions if len(value[1]) != 0]

#eventually authomaticall replace
#create dictionary of replacements
#better to have a dictionary for each city
cities = [value[0] for value in positions]
correspondences = {}
for key, value in place_name_dict.items():
    for key1, value1 in positions:
        if key1 == key:
            labour = {}
            if len(value1) == 1:
                guild1 = value[value1[0][0]]
                guild2 = value[value1[0][1]]
                labour[guild1] = guild2
                correspondences[key] = labour
            if len(value1) > 1:
                for n in range(0, len(value1)):
                    guild1 = value[value1[n][0]]
                    guild2 = value[value1[n][1]]
                    labour[guild1] = guild2
                    correspondences[key] = labour
    
#apply the modification
for key, dictionary in correspondences.items():
    mask = merged['place'] == key
    # Apply the mapping only to the 'guild_name' entries of these rows
    merged.loc[mask, 'guild_name'] = merged.loc[mask, 'guild_name'].replace(dictionary)
#50 guilds reduced
grouped = merged.groupby(['place', 'guild_name'])  
merged.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merge_senato_mocarelli1_ADJUSTED.xlsx")
