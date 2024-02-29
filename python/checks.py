# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 00:56:42 2023

@author: edobo
"""

import pandas as pd


p_mocarelli = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Mocarelli\db_mocarelli.xlsx"
mocarelli = pd.read_excel(p_mocarelli, header = 0)
p_check = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\check_senato_output.xlsx"
check = pd.read_excel(p_check, header = 0)
locality_mocarelli = list(mocarelli['Place'].unique())
locality_mocarelli =  locality_mocarelli[:-1]
locality_to_check = list(check['Place'].unique())

common_places = []
different_places = []
for place in locality_to_check:
    for places in locality_mocarelli:
        if place == places:
            common_places.append(place)
        else:
            different_places.append(place)
            
common_places = set(common_places)
different_places = set(different_places)
check_frequencies = check['Place'].value_counts()
check_mocarelli = mocarelli['Place'].value_counts()


columns_to_check = ['Place', 'Name of the guild']
merged_df = pd.merge(mocarelli, check , how='outer')
merged_df = merged_df[~merged_df.duplicated(subset=columns_to_check)]

    
frequencies = merged_df['Place'].value_counts()
merged_df.to_excel(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merging_attempt.xlsx')