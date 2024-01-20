# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 17:33:03 2024

@author: edobo
"""

import pandas as pd
import numpy as np
import xlsxwriter
import json
import math
from collections import defaultdict


def list_to_dict(lista, notnan = True):
    translator_dict = defaultdict(list)
    for key, value in lista:
        translator_dict[key].append(value)
    translator_dict = dict(translator_dict)
    if notnan == True:
        translator_dict = {key: [value for value in values if not (isinstance(value, float) and math.isnan(value))] 
                                 for key, values in translator_dict.items()}
        translator_dict = {key: values for key, values in translator_dict.items() if not (isinstance(key, float)
                                                                                          and math.isnan(key))}
    return translator_dict

def merge_dict(dict1, dict2):
    merged_dict = {key: dict1.get(key, []) + dict2.get(key, []) for key in set(dict1) | set(dict2)}
    return merged_dict