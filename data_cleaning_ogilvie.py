# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 21:10:34 2024

@author: edobo
"""

import pandas as pd
import os
import re
import numpy as np
#---personal modules
import sys
sys.path.append(r"C:\Users\edobo\OneDrive\Desktop\Python\modules")
from statistical_calculations import frequencies

ogilvie_path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Ogilvie\Database_for_Italy_ogilvie.xlsx"
ogilvie = pd.read_excel(ogilvie_path)
ogilvie.rename(columns={'Locality': 'place', 'Period': 'year', 'Occupation': 'guild_name'}, inplace=True)
#fix manually the "rimasugli" column
ogilvie[['guild_name', 'guild_name_ITA', 'rimasugli']] = ogilvie['guild_name'].str.split("(", expand=True)
ogilvie['guild_name_ITA'] = ogilvie['guild_name_ITA'].str.replace('(', '').str.replace(')', '').str.replace(',', ' ')
ogilvie.to_excel(ogilvie_path)

