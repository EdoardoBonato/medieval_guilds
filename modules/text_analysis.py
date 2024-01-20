# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 20:11:51 2024

@author: edobo
"""

import pandas as pd
import numpy as np
import xlsxwriter
import json
import sys
sys.path.append(r"C:\Users\edobo\OneDrive\Desktop\Python\modules")
from statistical_calculations import frequencies
import numpy as np
import math
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2

def similar_matrix_df(dataframe, columns = [], column_number = None, column_name = None):
    place_name_str = None
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v1')
    data = dataframe[columns]
    place_name_str = [str(row[columns[0]]) + ' ' + str(row[columns[1]]) for key, row in data.iterrows()]
    embedd = model.encode(place_name_str)
    similarity = cosine_similarity(embedd)
    return similarity

def threshold_change_df(dataframe, similarity_matrix, threshold = 0.8):
    threshold_up = 0.99
    # Find indices where values are higher than the threshold
    indices = np.where((threshold <= similarity_matrix) & (similarity_matrix < threshold_up))
    # Zip the row and column indices together
    positions = list(zip(indices[0], indices[1]))
    unique_tuples = list(set(frozenset(t) for t in positions))
    # Convert the unique frozensets back to tuples
    result_list = [tuple(fs) for fs in unique_tuples]
    similar_guilds = []
    for index_tuple in result_list:
        rows = dataframe.iloc[list(index_tuple)]
        similar_guilds.append(rows[['place', 'guild_name', 'year', 'year_']])
    similar_guilds = [dataframe for dataframe in similar_guilds if dataframe['place'].nunique() == 1]
    return similar_guilds

def find_similarity(matrix, treshold = 0.7):
    condition = (matrix > treshold) & (matrix < 0.97)
    # Focus on upper triangle, excluding the diagonal
    upper_triangle_indices = np.triu_indices_from(matrix, k=0)
    filtered_indices = np.where(condition[upper_triangle_indices])
    # Convert these indices back to the original matrix's coordinate system
    positions = [(upper_triangle_indices[0][i], upper_triangle_indices[1][i]) for i in filtered_indices[0]]
    return positions

    