import PyPDF2
import pandas as pd
import numpy as np
from collections import defaultdict
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import math
import sys
import json
sys.path.append(r"C:\Users\edobo\OneDrive\Desktop\medieval_guilds\modules")
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

path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\final_merging_attempt.xlsx"    
merged = pd.read_excel(path)

#divide the two datasets : the one with classification and the one without  
merged_with_classification = merged[merged['categorization'].notna()]
merged_without_classification = merged[merged['categorization'].isna()] 

#get the unique values of guild_name
mestieri = set(merged_with_classification['guild_name'])
mestieri_without_classification = set(merged_without_classification['guild_name'])

#try to see if we are missing some unskilled guilds, using text analysis
model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v1')
embedded_mestieri = [(mestiere, model.encode(mestiere)) for mestiere in mestieri]
embedded_mestieri = list_to_dict(embedded_mestieri)
embedded_mestieri_without_classification = [(mestiere, model.encode(mestiere)) for mestiere in mestieri_without_classification
                                            if isinstance(mestiere, str)]
embedded_mestieri_without_classification = list_to_dict(embedded_mestieri_without_classification)   

lista = compare_dict(embedded_mestieri, embedded_mestieri_without_classification, treshold = 0.7)

#we found some unskilled guilds that are not in the classification
#we select the ones that "makes sense"
lista = [lista[1], lista[2], lista[3], lista[4], lista[5], lista[6], 
         lista[7], lista[8], lista[9], lista[16], lista[17], lista[18],
         lista[21], lista[23], lista[24], lista[25], lista[26], lista[27], 
         lista[28], lista[29], lista[33], lista[34], lista[36], lista[37],
         lista[38], lista[39], lista[40]]

#find the corresponding classification for each guild
classification = [(classification, mestiere) for mestiere, classification in
                   merged_with_classification[['guild_name', 'categorization']].values]
classification = list_to_dict(classification)
classification = {key : set(value) for key, value in classification.items()}   
lista_to_add = []
for mestiere, mestiere1 in lista:
    for key, value in classification.items():
        if mestiere in value:
            coppia = (mestiere1, key)
            lista_to_add.append(coppia)    
lista_to_add = list_to_dict(lista_to_add)
# Add the new classification to the old one      
merged['categorization'] = merged.apply(lambda row: lista_to_add.get(row['guild_name'], np.nan) if pd.isna(row['categorization'])
                                         else row['categorization'], axis=1)
merged['categorization'] = merged['categorization'].apply(lambda x: x[0] if isinstance(x, list) else x)

#now all the unskilled guilds are classified
#create a dummy variable for the skilled guilds
merged['unskilled'] = merged['categorization'].apply(lambda x: 0 if pd.isna(x) else 1)

#export the dataset
merged.to_excel(path)   
#end of the snippet
