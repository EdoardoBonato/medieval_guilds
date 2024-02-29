# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 12:33:58 2023

@author: edobo
"""
import pandas as pd
import numpy as np
import math
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2

with open(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Literature\guilds_sicily_lombardo.pdf", 'rb') as file:
    # Read the PDF text
    pdf_text = ""
    pdf_reader = PyPDF2.PdfReader(file)
    for page_num in range(len(pdf_reader.pages)):
        pdf_text += pdf_reader.pages[page_num].extract_text()
        
model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v1')
        
# Token
pdf_sentences = pdf_text.split('.')
pdf_sentences = pdf_sentences[1000 : ]
pdf_sentences = [sentence for sentence in pdf_sentences if len(sentence) >= 5]


similarities = []
typical_sentences = ["The number of guilds in [specific place] during [time period] was significant.",
    "Historical records indicate the presence of  guilds in Italy",
    "In city, the guild system thrived, boasting the  number of guilds.",
    "During century, the guilds played a crucial role",
    "A document from year mentions the existence of guilds in locality.",
    "Guilds were an integral part of the economy, with records showing guilds in operation.",
    "The economic landscape of italy was characterized by the presence of  guilds during century",
    "Reports from year highlight the diversity and strength of  guilds",
    "Archival sources reveal that city was home to guilds in the century",
    "The guilds were pivotal to the economic structure of place in year"]

typical_embedd = model.encode(typical_sentences)


for sentence in pdf_sentences:
    embedding_pdf = model.encode(sentence)
    embedding_pdf = embedding_pdf.reshape(1, -1)
    final = np.append(typical_embedd, embedding_pdf, axis = 0)
    similarity_matrix = cosine_similarity(final)
    correspondences = similarity_matrix[10 , :] 
    correspondences = correspondences[:-1]
    similarities.append((sentence, correspondences))

interesting_sentences = []
for tuples in similarities:
    for value in tuples[1]:
        if value >= 0.7:
            interesting_sentences.append((tuples[0], tuples[1]))
            break
 
