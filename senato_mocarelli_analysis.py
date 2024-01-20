# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 19:10:18 2023

@author: edobo
"""

import pandas as pd
import numpy as np
import xlsxwriter
import json
import re
import PyPDF2

data_path = r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merging_attempt.xlsx'
data = pd.read_excel(data_path)

duplicated = data.duplicated(subset = ['Name of the guild', 'Place'])
frequencies = data['Place'].value_counts()
relative_frequencies = frequencies / frequencies.sum()
frequencies_data = pd.concat([frequencies, relative_frequencies], keys = ['nr', 'weights'], axis = 1)

frequencies_mocarelli = pd.read_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Mocarelli\db_mocarelli.xlsx", sheet_name = 'weights')
frequencies_mocarelli.set_index('Place', inplace = True)

difference = frequencies_mocarelli['weights'] - frequencies_data['weights']

all_freq = pd.merge(frequencies_data, frequencies_mocarelli, left_index = True, right_index = True, how = 'inner')

