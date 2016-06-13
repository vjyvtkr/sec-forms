# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 14:09:22 2016

@author: u505123
"""

import pandas as pd

path = "C:\\Users\\u505123\\Documents\\Project\\Dataset\\10_K\\"
fileName = "outt3301"
df = pd.read_csv(path+fileName+".csv",",")
x = df['fact']
x.to_csv(path+fileName+"_fact.csv")