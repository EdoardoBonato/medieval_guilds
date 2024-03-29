#from the extended datasets obtain the grouped version
#the extended version contains all observations, i.e. every year in which every guild is observed
#the gruoped version will have as observation the number of guilds, with their year of born and death

import PyPDF2
import pandas as pd
import numpy as np
from collections import defaultdict
import sys
sys.path.append(r"C:\Users\edobo\OneDrive\Desktop\Python\modules")
from data_structures import list_to_dict
from data_structures import merge_dict
from statistical_calculations import frequencies
from text_analysis import find_similarity
import random
from text_analysis import find_similarity, compare_dict

#import merged datasets
path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merged_w_abolition1_region.xlsx"
merged = pd.read_excel(path)

#keep only the information about the abolished guilds
merged = merged[(merged.change == 'IS ABOLISHED') | (merged['change'].isna())]
#clean from no sense values
merged = merged[merged['combined_years'] != 0]

grouped = merged.groupby(['place', 'guild_name'])
grouped_min_max = grouped.agg({'region': 'first', 'combined_years' : ['min', 'max']})
def approximate_year(year):
    return round(year / 50) * 50
grouped_min_max[['group_min', 'group_max']] = grouped_min_max['combined_years'].apply(approximate_year)
grouped_min_max = grouped_min_max.reset_index()
grouped_min_max.columns = ['place', 'guild_name','region', 'min_year', 'max_year', 'group_min', 'group_max']

#calculate average duration
grouped_min_max['duration'] = grouped_min_max['max_year'] - grouped_min_max['min_year']
calculate_duration = grouped_min_max[grouped_min_max.duration > 20]
average_duration = np.mean(calculate_duration['duration'])

#export to dataset
grouped_min_max = grouped_min_max.sort_values(by = 'duration', ascending = False)   
grouped_min_max.to_excel(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\grouped_min_max1_region.xlsx')
