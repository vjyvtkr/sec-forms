# -*- coding: utf-8 -*-
"""
Created on Wed Jun 01 14:23:16 2016

@author: Vijay Yevatkar
"""

import pandas as pd
import re
import nltk

df = pd.read_csv('C:\\Users\\u505123\\Documents\\Project\\Output\\testing_3.csv','|')

text = []
for i in df['fact']:
    text.append(i)



'''
sales = []
revenue = []

for i in text:
    if 'sales' in i:
        sales.append(i)
    elif 'revenue' in i:
        revenue.append(i)

s_dict = {}
r_dict = {}
for i in sales:
    s_dict[i] = [m.start() for m in re.finditer('sales', i)]
for i in revenue:
    r_dict[i] = [m.start() for m in re.finditer('revenue', i)]

'''