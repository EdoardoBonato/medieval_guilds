# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 15:59:43 2024

@author: edobo
"""


import pandas as pd
import numpy as np
import xlsxwriter
import json
import numpy as np
import math
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import sys
sys.path.append(r"C:\Users\edobo\OneDrive\Desktop\Python\modules")
from data_structures import list_to_dict
from data_structures import merge_dict
from statistical_calculations import frequencies
import ast

path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\ogilvie_translation_advanced - Copia.xlsx"
ogilvie = pd.read_excel(path)

#due to bad managament of data, now the direct translation given by the ogilvie will be taken from a precedent
#version of the file ogilvie_translation_advanced and implemented to the newest version
#extract the translation from the english name [Apothecaries(speziali)]
#save it in a new column
#fix manually the "rimasugli" column
ogilvie[['guild_name', 'guild_name_ITA', 'rimasugli']] = ogilvie['guild_name'].str.split("(", expand=True)
ogilvie['guild_name_ITA'] = ogilvie['guild_name_ITA'].str.replace('(', '').str.replace(')', '').str.replace(',', ' ')
#import 
ogilvie_translation_path = r'C:/Users/edobo/OneDrive/Desktop/Thesis/Medieval Guilds/Data/EDITED_db/Merge/ogilvie_translation_advanced.xlsx'
ogilvie_translation = pd.read_excel(ogilvie_translation_path)

ogilvie_translation['guild_name_ITA'] = ogilvie['guild_name_ITA']

ogilvie_translation.to_excel(ogilvie_translation_path)