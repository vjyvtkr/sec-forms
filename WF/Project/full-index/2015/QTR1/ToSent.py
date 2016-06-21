# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 14:56:58 2016

@author: Vijay Yevatkar
"""

import pandas as pd
import re
import unidecode as ud
import nltk

sent_count_list = []
pathIs = 'C:\\Users\\u505123\\Documents\\Project\\Dataset\\10_K\\'
oPath = 'C:\\Users\\u505123\\Documents\\Project\\Dataset\\10_K\\Output\\OPFinal_Cost\\'
sentences = []
for c in range(15,22):
    countIs = 2101 + c*300
    fileIs = pathIs+"outt"+str(countIs)+".csv"
    oFileIs = oPath+"outt"+str(countIs)+"_sent.csv"
    print "Processing:",fileIs    
    df = pd.read_csv(fileIs, ',')  
    facts = list(df['fact'])
    sal_rev_per = set()
    cname_list = []
    cik_list = []    
    qtr = []
    ftype = []
    date_list = []
    path_list = []
    counter = 0    
    for i in facts:
        ttype = df['form_type'].ix[counter]
        t_fact = re.sub(r'<.*?>',' ',str(i))
        t1_fact = re.sub(r'\s+',' ', t_fact)
        t_fact = ud.unidecode(t1_fact)
        t1_fact = re.sub(r'&#[a-zA-Z]*\d+;|&[a-zA-Z]+;', ' ', t_fact)
        p1 = re.compile(r'sale|revenue')
        p2 = re.compile(r'%|percent')
        p3 = re.compile(r'represent|account|attribute|contribute')
        p4 = re.compile(r'cost of revenue')
        t_result = nltk.sent_tokenize(t1_fact)
        for j in t_result:
            if not p4.search(j) and p3.search(j) and p2.search(j) and p1.search(j):
                before = len(sal_rev_per)                        
                sal_rev_per.add(j)
                after = len(sal_rev_per)
                if before != after:
                    sentences.append(j)
                    cname_list.append(df['Company_Name'].ix[counter])
                    cik_list.append(df['CIK'].ix[counter])
                    qtr.append(df['qtr'].ix[counter])
                    ftype.append(ttype)
                    date_list.append(df['Date.Filed'].ix[counter])
                    path_list.append(df['Path'].ix[counter])
        counter=counter+1
    df2 = pd.DataFrame(columns = ['qtr', 'Form_Type', 'Company_Name', 'CIK', 'Date', 'Path', 'Indicator', 'Phrase'])
    df2['qtr'] = qtr
    df2['Form_Type'] = ftype
    df2['Company_Name'] = cname_list
    df2['CIK'] = cik_list
    df2['Date'] = date_list
    df2['Path'] = path_list
    no_list = ['No' for i in range(0,len(cik_list))]
    df2['Indicator'] = no_list
    df2['Phrase'] = list(sal_rev_per)
    t_count = df2['Phrase'].__len__()
    sent_count_list.append(t_count)
    df2.to_csv(oFileIs) 
    print "Processed %s to %s\n"%(fileIs,oFileIs)

