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

folder_path = r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\senato'

pdf_files = [file for file in os.listdir(folder_path) if file.endswith('.pdf')]



pdfs_text = {}
url = r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\senato'
dates = {}

for pdf_file in pdf_files:
    pdf_path = url + '\\' + pdf_file
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
            dates[pdf_file] = date
        except Exception as e:
            continue

dates_dict = {key : [int(value) for  value in values] for key, values  in dates.items()}

for key,values in dates_dict.items():
    for value in values:
        if value >= 1897:
            values.remove(value)

dates_dict = {key: sorted(value) for key, value in dates_dict.items()}

for key, values in dates_dict.items():
    dates_dict[key] = set(values)



senato = pd.DataFrame.from_dict(dates_dict, orient ='index')
#senato['Place'] = senato.index.map(lambda filename: filename.split(' ')[0])
senato.set_index('Place', inplace=True)
senato.index = senato.index.str.upper()
senato = senato.reset_index()

senato_to = pd.read_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\check_senato_output.xlsx")

senato_merged = pd.concat([senato, senato_to], axis = 1)
senato_merged.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\Merge\senato_integration_base.xlsx")