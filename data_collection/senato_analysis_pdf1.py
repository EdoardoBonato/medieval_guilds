# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 22:42:19 2024

@author: edobo
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 16:29:57 2023

@author: edobo
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl
import os
import re
import PyPDF2
import pytesseract
from PIL import Image
import sys
from pdf2image import convert_from_path, convert_from_bytes
import tempfile
import pytesseract
import json


# Add the path to the list of paths
new_path = r'C:\Program Files\Tesseract-OCR'
sys.path.append(new_path)

senato_to = pd.read_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\check_senato_output1.xlsx")
folder_path = r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\senato1'

pdf_files = [file for file in os.listdir(folder_path) if file.endswith('.pdf')]
 


pdfs_text = {}
url = r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\senato1'
dates = {}

for pdf_file in pdf_files:
    pdf_path = url + '\\' + pdf_file
    name = os.path.splitext(pdf_file)[0]
    # Use regular expression to remove numbers
    name = re.sub(r'\d+', '', name)
    try:
        images = convert_from_path(pdf_path)
    except Exception as e:
        continue
    
    
    for i, image in enumerate(images):
        
        try:
            # Convert the image to RGB format
            image = image.convert('RGB')
            textz = pytesseract.image_to_string(image)
            pdfs_text[pdf_file] = textz
            date = re.findall(r'\b\d{4}\b', textz)
            dates[name] = date
        except Exception as e:
            continue


with open(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\hi.json', 'w') as file:
    json.dump(dates, file)
    
dates_dict = {key : [int(value) for  value in values] for key, values  in dates.items()}

dates_dict = {key : [value for value in values if int(value) < 1860] for key, values in dates.items() }

dates_dict = {key: sorted(value) for key, value in dates_dict.items()}

for key, values in dates_dict.items():
    dates_dict[key] = set(values)

#set the dataframe for the date
senato = pd.DataFrame.from_dict(dates_dict, orient ='index')
senato = senato.reset_index()
senato= senato.rename(columns = {'index' : 'place'})
senato['place'] = senato['place'].str.upper()
senato[['guild_name', 'place']] = senato['place'].str.split("_", expand=True)
#set the datasets for the names
senato_to = senato_to.rename(columns = {'Place' : 'place', 'Name of the guild' : 'guild_name'})
senato_to['place'] = senato_to['place'].str.upper()
senato_to['guild_name'] = senato_to['guild_name'].str.upper()
senato_to = senato_to.drop(columns = 'Unnamed: 0')
senato_to = senato_to.drop_duplicates()
#merged the dataset
senato_merged = pd.merge(senato, senato_to, on = ['place', 'guild_name'], how = 'inner')
columns = senato_merged.columns.to_list()
columns = [columns[-1]] + columns[0:27]
senato_merged = senato_merged[columns]
senato_merged.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\senato_integration_base1.xlsx")





