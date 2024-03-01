# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 21:02:24 2023

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

mocarelli_path = r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Mocarelli\db_mocarelli.xlsx'
mocarelli = pd.read_excel(mocarelli_path, sheet_name = 'Data_w_region')
mocarelli['guild_name'] = mocarelli['guild_name'].str.upper()
senato_path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\senato_integration_base1.xlsx"
senato = pd.read_excel(senato_path)

#see common guilds
common_guilds = pd.merge(mocarelli, senato, on = ['place', 'guild_name'], how = 'inner')
common_guilds = common_guilds[['place', 'guild_name']]

#merging operation
merged = pd.merge(mocarelli,senato, how= 'outer')
merged['guild_name'] = merged['guild_name'].str.upper()
#merged = merged.drop(['Unnamed: 0', 'Unnamed: 23', 'Unnamed: 24'], axis = 1)


frequencies_data = frequencies(merged['place'])

cities = merged['place'].unique()
columns = merged.columns.to_list()


#rename year columns
numerical_columns = [column for column in columns if isinstance(column, int)]
rename_function = ['year'+ str(column) for column in numerical_columns]
merged = merged.rename(columns = dict(zip(numerical_columns, rename_function)))
columns = merged.columns.to_list()
#reordered_columns = columns[0:16] + columns[24:] + columns[16 : 24]
#merged = merged[reordered_columns]
duplicate_rows = merged[merged.duplicated(subset=['place', 'guild_name'])]

#different merging technique
merged_try = pd.merge(mocarelli, senato, on = ['place', 'guild_name'], how = 'outer')
duplicate_rows_try = merged_try[merged_try.duplicated(subset=['place', 'guild_name'])]
columns_try = merged_try.columns.to_list()
numerical_columns_try = [column for column in columns_try if isinstance(column, int)]
rename_function_try = ['year'+ str(column) for column in numerical_columns_try]
merged_try = merged_try.rename(columns = dict(zip(numerical_columns_try, rename_function_try)))
columns_try = merged_try.columns.to_list()
#reordered_columns_try = columns_try[0:17] + columns_try[30:] + columns_try[17 : 30]
#merged_try = merged_try[reordered_columns_try]
#interesting_columns_name = reordered_columns_try[17 : 118]

#try to group
grouped = merged_try.groupby(['guild_name', 'place'])
partial_merge = {}
partial_merge_df = pd.DataFrame()
for name, group in grouped:
    # Concatenate the 'year' columns for each group
    concatenated_years = pd.Series(group.filter(like='year').values.flatten(), name=name)
    if concatenated_years.isnull().all() == False:
        concatenated_years = concatenated_years.dropna().drop_duplicates()
        concatenated_years = concatenated_years[(concatenated_years >= 800) & (concatenated_years <= 1800)].sort_values()
        # Create a DataFrame for the current group with the concatenated years and the name and place
        current_group_df = pd.DataFrame({'name': name[0], 'place': name[1], 'years': [concatenated_years.values]})
        # Append the current group's DataFrame to the concatenated results DataFrame
        partial_merge[name] = current_group_df
        partial_merge_df = pd.concat([partial_merge_df, current_group_df], ignore_index=True)

total_merge = {}
total_merge_df = pd.DataFrame()
for name, group in grouped:
    # Concatenate the 'year' columns for each group
    concatenated_years = pd.Series(group.filter(like='year').values.flatten(), name=name)
    concatenated_years = concatenated_years.dropna().drop_duplicates()
    concatenated_years = concatenated_years[(concatenated_years >= 800) & (concatenated_years <= 1800)].sort_values()
    # Create a DataFrame for the current group with the concatenated years and the name and place
    current_group_df = pd.DataFrame({'guild_name': name[0], 'place': name[1], 'years': [concatenated_years.values]})
    # Append the current group's DataFrame to the concatenated results DataFrame
    total_merge[name] = current_group_df
    total_merge_df = pd.concat([total_merge_df, current_group_df], ignore_index=True)

total_merged = pd.merge(mocarelli, total_merge_df, on = ['place', 'guild_name'], how = 'outer')
total_merged['col'] =total_merged['years'].astype(str)
t_years_extracted = total_merged['col'].str.extractall(r'(\b\d{4}\b)')
t_years_pivoted = t_years_extracted.unstack()
t_years_pivoted.columns = ['year' + str(value2) if value2 != 0 else 'year_' for value1, value2 in t_years_pivoted.columns]
total_merged = pd.concat([total_merged, t_years_pivoted], axis = 1 )
total_merged = total_merged.drop(columns = ['years', 'col'])
total_merged['year_'] = total_merged['year_'].astype(float)
total_merged['year'] = total_merged['year'].astype(float)
mask = total_merged['year'].notna() & total_merged["year_"].notna()
#Create a new column indicating if the non-NaN values are equal
total_merged.loc[mask, 'check_discrepancy'] = total_merged.loc[mask, 'year'] == total_merged.loc[mask, 'year_']
total_merged['check_discrepancy'] = total_merged['check_discrepancy'].apply(lambda x: x if np.isnan(x) else (1 if x == True else 0))
total_merged['check_discrepancies'] = [np.nan if np.isnan(value['year']) or np.isnan(value['year_'])
                                       else( 1 if value['year'] - 20 < value['year_'] < value['year'] + 20 else 0)
                                       for index, value in total_merged.iterrows()]

partial_merge_df['col'] = partial_merge_df['years'].astype(str)
years_extracted = partial_merge_df['col'].str.extractall(r'(\b\d{4}\b)')
years_pivoted = years_extracted.unstack()
years_pivoted.columns = ['year' + str(value2) if value2 != 0 else 'year_' for value1, value2 in years_pivoted.columns]
new_datas = pd.concat([partial_merge_df, years_pivoted], axis=1)
new_datas = new_datas.drop(columns = ['years', 'col'])

total_merged.to_excel(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merge_senato_mocarelli1.xlsx')
merged_try.to_excel(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\merge_senato_mocarelli_try1.xlsx')
