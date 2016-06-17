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
oPath = 'C:\\Users\\u505123\\Documents\\Project\\Dataset\\10_K\\Output\\OPFinal\\'
sentences = []
for c in range(0,22):
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
    #pattern = re.compile(r'sales|revenue')
    counter = 0    
    for i in facts:
        ttype = df['form_type'].ix[counter]
        #if ttype is '10-K' or ttype is '10-Q': 
        #ans = pattern.search(str(i))
        #if ans: 
        t_fact = re.sub(r'<.*?>',' ',str(i))
        t1_fact = re.sub(r'\s+',' ', t_fact)
        t_fact = ud.unidecode(t1_fact)
        t1_fact = re.sub(r'&#\d+;|&[a-zA-Z]+;', ' ', t_fact)
        #t1_fact = re.sub(r'&#8217;', "'", t_fact)
        
        t_result = nltk.sent_tokenize(t1_fact)
        for j in t_result:
            if 'sale' in j or 'revenue' in j:
                if '%' in j or 'percent' in j:
                    if 'represent' in j or 'account' in j or 'attribute' in j or 'contribute' in j:
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
    df2['Indicator'] = 'NA'
    df2['Phrase'] = list(sal_rev_per)
    t_count = df2['Phrase'].__len__()
    sent_count_list.append(t_count)
    df2.to_csv(oFileIs,"|") 
    print "Processed %s to %s\n"%(fileIs,oFileIs)

