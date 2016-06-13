# -*- coding: utf-8 -*-
"""
Created on Tue May 24 12:36:13 2016
@author: Vijay Yevatkar
"""
import pandas as pd
from bs4 import BeautifulSoup
import os
import re
import unidecode as ud

'''
Function to extract the follwing information from a given 10K Form.
['elementId','contextId','unitId','fact','decimals','scale','sign','factId','ns','cik','companyName','formType']
Input = XML File to be parsed.
Output = Returns a DataFrame and also writes it to a csv file to the given path.
Parameters = Input File Path and Output File Path (both absolute)
'''

#def ExtractID(inpName, outpName, cik, cname, form_type):
inpName = "C:\\Users\\u505123\\Documents\\Project\\Dataset\\hrl-20151025.xml"
outpName = "C:\\Users\\u505123\\Documents\\Project\\Output\\testing_3.csv"
cik = '1234'
cname = 'abcd'
form_type = '10-K'

#check if file exists
try:
    f = open(inpName)
    f.close()
except IOError:
    print

#beautifulsoup object
inp = BeautifulSoup(open(inpName))

#columns that need to be extracted (3 more will be added later)
columns = ['elementId','contextId','unitId','fact','decimals','scale','sign','factId','ns']
#Empty DataFrame. We will return this finally.
df = pd.DataFrame([],columns=columns)

#Elements that need to be extracted are those which are specified in the xmlns values.

temp_ns = inp.find('xbrl')
if temp_ns is None:
    ns = inp.find('xbrli:xbrl').attrs
else:
    ns = temp_ns.attrs
#corresponding id's
check ='contextref'
un = 'unitref'
dec = 'decimals'
fin_text_list = []
fin_text_string_list = []

#iterate over each tag in the file
for i in inp.find_all():
    rows = []
    ns_val = ''
    #Check the name of the tag.
    ns_check = i.name.split(":")[0]

    #If the name exists in the list, we need to parse it else continue.
    if check in i.attrs:

        #name is the elementid
        rows.append(i.name)

        #contextid is "contextref"
        rows.append(i[check])

        #un is the unitref corresponding to the unitid
        if un in i.attrs:
            rows.append(i[un])
        else:
            rows.append('')

        #text corresponds to the fact.
        act_text = ud.unidecode(i.text)
        nextObj = BeautifulSoup(act_text)
        fin_text_string = ''
        try:
            fin_text_string += ud.unidecode(nextObj.find_all()[0].text)
        except:
            fin_text_string += ''

        rows.append(ud.unidecode(fin_text_string))
        fin_text_list.append(ud.unidecode(fin_text_string))

        #dec is the decimals attribute
        if dec in i.attrs:
            rows.append(i[dec])
        else:
            rows.append('')

        #empty for now, need to be replaced by the corresponding scale, sign, factId, etc.
        rows.append("")
        rows.append("")
        rows.append("")

        #ns_val, as the name suggests, is the ns attribute
        for k in ns.keys():
            if ns_check in k:
                ns_val = ns[k]
                break

        rows.append(ns_val)

        #These values are appended to the dataframe created earlier.
        f_rows = [rows]
        df2 = pd.DataFrame(f_rows,columns=columns)
        frames = [df,df2]
        x = pd.concat(frames)
        df = x

#Indices are made proper.
indices = pd.DataFrame(range(0,df['elementId'].count()),columns=['index'])
df = df.set_index(indices['index'])

#Append the company name, form type and cik
df['cik'] = cik
df['companyName'] = cname
df['formType'] = form_type

sentences = []
for i in fin_text_list:
    if len(i)>10:
        #x = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s',i)
        x = re.split(r'(\. [A-Z])',i)
        sentences.append(x)

flattened = [val for sublist in sentences for val in sublist]

final_count=[]
for i in flattened:
    x = " ".join((i).split())
    if x!='':
        final_count.append(x)

if final_count[0][0]=='.':
    ffinal_count = []
else:
    ffinal_count=[final_count[0]]
i=1
while True:
    if i>=len(final_count):
        break
    if final_count[i][0]=='.':
        i=i+1
        continue
    if final_count[i-1][0]=='.':
        temp = str(final_count[i-1][2])
        ffinal_count.append(temp+final_count[i])
    else:
        ffinal_count.append(final_count[i])
    i = i+1


revenue=[]
for i in ffinal_count:
    if 'revenue' in i and 'represent' in i:
        revenue.append(i)

print revenue

#Output the created DataFrame to csv and return the DataFrame
if not os.path.exists(outpName):
    df.to_csv(outpName,"|")
else:
    with open(outpName, 'a') as f:
        df.to_csv(f, sep="|", header=False)
