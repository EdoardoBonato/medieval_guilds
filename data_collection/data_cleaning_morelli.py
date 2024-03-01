# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 10:52:57 2023

@author: edobo
"""

import random
import statistics
import math
import numpy as np ###linear algebra
import time
import pandas as pd ###importare file da excel
import openpyxl
import statsmodels  ###analisi dei dati avanzata
import itertools  
import matplotlib.pyplot as plt ###grafici
import seaborn as sns ### plot package
from datetime import datetime,timedelta
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import os
import xlsxwriter

#import database morelli RAW
mocarelli = pd.read_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\Database_mocarelli.xlsx", header = 0)
column = mocarelli['Place']
country_mapping = {'ITA' : 'Italy', 'ITALY' : 'Italy', 'TALY' : 'Italy', 'italy' : 'Italy' , 'Italy' : 'Italy'}
place_mapping =  {'ALESSANDRIA' : 'ALESSANDRIA', 'ANCONA': 'ANCONA', 'ASCOLI PICENO' : 'ASCOLI PICENO', 'ASTI' : 'ASTI', 'Ancona' : 'ANCONA', 'Arezzo': 'AREZZO', 'BERGAMO': 'BERGAMO', 'BOLOGNA': 'BOLOGNA', 'BRESCA' : 'BRESCIA', 'BRESCIA' : 'BRESCIA', 'Borgo a Mozzarino' : 'BORGO A MOZZARINO', 'CAGLIARI': 'CAGLIARI', 'CATANIA': 'CATANIA', 'CHIOGGIA': 'CHIOGGIA', 'COMO' : 'COMO', 'CREMONA': 'CREMONA', 'Cagliari': 'CAGLIARI', 'Camerino': 'CAMERINO','Carpi': 'CARPI', 'Catanzaro' : 'CATANZARO', 'Cesena': 'CESENA', 'Crema': 'CREMA', 'ESTE': 'ESTE', 'FAENZA': 'FAENZA', 'FERRARA': 'FERRARA', 'FIRENZE': 'FIRENZE', "FORLI'" : "FORLI'", 'Fabriano':'FABRIANO', 'GENOVA': 'GENOVA', 'Gubbiio': 'GUBBIO', 'Gubbio':'GUBBIO', 'LODI':'LODI', 'LUCCA': 'LUCCA', 'MANTOVA': 'MANTOVA', 'MESSINA': 'MESSINA', 'MILANO':'MILANO', 'MODENA': 'MODENA', 'MONSELICE':'MONSELICE','Macerata': 'MACERATA', 'NAPOLI': 'NAPOLI', 'Narni': 'NARNI','Oristano':'ORISTANO', 'Orvieto': 'ORVIETO', 'PADOVA': 'PADOVA', 'PALERMO':'PALERMO', 'PARMA':'PARMA', 'PAVIA':'PAVIA', 'PIACENZA':'PIACENZA', 'PISA':'PISA','Padova':'PADOVA', 'Pesaro':'PESARO', 'Pordenone':'PORDENONE', 'REGGIO EMILIA': 'REGGIO EMILIA', 'ROMA':'ROMA', 'Recanati': 'RECANATI', 'SASSARI': 'SASSARI', 'SAVONA':'SAVONA', 'SIENA':'SIENA', 'Salemi':'SALEMI', 'TORINO':'TORINO', 'TRAPANI':'TRAPANI', 'TREVISO':'TREVISO', 'Torre del Grego':'TORRE DEL GRECO', 'Trapani':'TRAPANI', 'Trento':'TRENTO', 'UDINE':'UDINE', 'VENEZIA':'VENEZIA', 'Venice':'VENEZIA', 'VENICE': 'VENEZIA','VERONA':'VERONA', 'VICENZA':'VICENZA', 'VITERBO':'VITERBO','orvieto':'ORVIETO', 'palermo':'PALERMO', 'treviso':'TREVISO', 'udine':'UDINE'}
mocarelli['Country'] = mocarelli['Country'].map(country_mapping)
mocarelli['Place']= mocarelli['Place'].map(place_mapping)
missing_values_count = mocarelli.isnull().sum()
mocarelli.dropna(axis = 1, how = "all", inplace = True)
mocarelli.rename(columns={'Place': 'place', 'Year': 'year', 'Name of the guild': 'guild_name'}, inplace=True)
writer = pd.ExcelWriter(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Mocarelli\mocarelli_clean.xlsx", engine = "xlsxwriter", mode ="w")
mocarelli.to_excel(writer, sheet_name = "Data")
missing_values_count.to_excel(writer, sheet_name = "missing_value")
writer.close()
