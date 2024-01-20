# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 19:05:58 2024

@author: edobo
"""

import os
import pandas as pd


def frequencies(data):
    
    frequencies = data.value_counts()
    relative_frequencies = frequencies / frequencies.sum()
    frequencies_data = pd.concat([frequencies, relative_frequencies], keys = ['nr', 'weights'], axis = 1)
    
    return frequencies_data