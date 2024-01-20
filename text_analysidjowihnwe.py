# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 19:50:22 2023

@author: edobo
"""

import pandas as pd
import numpy as np
import math
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2

model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v1')

typical_sentences = ["The number of guilds in [specific place] during [time period] was significant.",
    "Historical records indicate the presence of [X] guilds in [specific place]",
    "In [specific place], the guild system thrived, boasting [X] number of guilds.",
    "During [time period], the guilds of [specific place] played a crucial role, with [X] in existence.",
    "A document from [year] mentions the existence of [X] guilds in [specific place].",
    "Guilds were an integral part of [specific place]'s economy, with records showing [X] guilds in operation.",
    "The economic landscape of [specific place] was characterized by the presence of [X] guilds during [time period].",
    "Reports from [year] highlight the diversity and strength of [specific place]'s guilds, numbering [X].",
    "Archival sources reveal that [specific place] was home to [X] guilds in the [time period].",
    "The guilds, numbering [X], were pivotal to the economic structure of [specific place] in [year]."]

typical_embedd = model.encode(typical_sentences)

sentence = 'il cielo è blu'

sentence_embedd = model.encode(sentence)
sentence_embedd = sentence_embedd.reshape(1, -1)
embed = np.append(typical_embedd, sentence_embedd, axis = 0)

similarities = [values for values in similarities if values[0] > 0.65]
p_ogilvie = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Ogilvie\Database_for_Italy_ogilvie.xlsx"
p_mocarelli = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Mocarelli\db_mocarelli.xlsx"
ogilvie = pd.read_excel(p_ogilvie, header = 0)
mocarelli = pd.read_excel(p_mocarelli, header = 0)
locality_ogilvie = list(ogilvie['Locality'].unique())
locality_mocarelli = list(mocarelli['Place'].unique())
locality_mocarelli =  locality_mocarelli[:-1]

common_places = []
different_places = []
for place in locality_mocarelli:
    for places in locality_ogilvie:
        if place in places:
            common_places.append(place)
        else:
            different_places.append(place)
            
common_places = set(common_places)
different_places = set(different_places)