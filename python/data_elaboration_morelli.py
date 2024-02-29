# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 13:17:06 2023

@author: edobo
"""

import pandas as pd
import numpy as np
import xlsxwriter
import json
#import dataset
db_mocarelli = pd.read_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Mocarelli\db_mocarelli.xlsx", header = 0)

print(db_mocarelli.nunique())

#want to move sth to xl? Append it!
excel = []
#observation by place
by_place = db_mocarelli.groupby("Place")
guilds_by_place = by_place["GuildsID"].count()
excel.append("guilds_by_place")
#nr og guilds by year(group)
by_year = db_mocarelli.groupby("Group")
places_for_years = by_year["GuildsID"].count()

#year_by_year_change(new guilds)
change_by_years = by_year["GuildsID"].count().pct_change()
excel.append("change_by_years")
#actual number of guilds by year
total_number_by_years = places_for_years.cumsum()
excel.append("total_number_by_years")
#change in number of guilds by year
total_change_by_years = total_number_by_years.pct_change()
excel.append("total_change_by_years")
#mapping municipality to region
comuni_italiani = pd.read_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\Elenco-comuni-italiani.xls", header = 0)
for names in comuni_italiani.columns:
    names.replace(" ", "")
comuni_corr = comuni_italiani[["Place", "Denominazione regione"]]
db_mocarelli_merged = db_mocarelli.merge(comuni_corr, how='left', on ='Place')
#guilds by region
by_region = db_mocarelli_merged.groupby("Denominazione regione")
guilds_by_region = by_region["GuildsID"].count()



string = "vigneri (vignaiuoli), lavoraturi, urtulani, burdunari (mulattieri), tabernari, vaccari, vucheri (beccai), putigari (bottegai o pizzicagnoli), curdari, ferrari e armeri, maniscalchi, muraturi, carpenteri, mirceri(mercial), sellari, conzaturi (conciatori), corredaturi (fabbricanti di corredi), curbiseri (ciabattini), planellari (fabbricanti di pianelle), pellicheri (pellicciai), cimaturt (misuratori di vino), custwureri (sarti), barberi, argenteri"
string = string.replace(",", "")
lista = list(string.split(" "))

#bring all to excel
writer = pd.ExcelWriter(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Mocarelli\db_mocarelli.xlsx", engine = "xlsxwriter", mode ="w")
db_mocarelli.to_excel(writer, sheet_name = "Data")
db_mocarelli_merged.to_excel(writer, sheet_name = "Data_w_region")
guilds_by_place.to_excel(writer, sheet_name = "guilds_for_place")
total_number_by_years.to_excel(writer, sheet_name = "guilds_by_year")
change_by_years.to_excel(writer, sheet_name = "change_by_year")
total_change_by_years.to_excel(writer, sheet_name = "total_change")
guilds_by_region.to_excel(writer, sheet_name = "total_number_by_region")
writer.close()


"""

"""

"""for df in excel:
    df.to_excel(writer, sheet_name = df)
writer.close()"""
"""
"""
    
