# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 15:30:55 2016

@author: u505123
"""

from sklearn.pipeline import Pipeline
import pandas as pd
from sklearn.cross_validation import KFold
from sklearn.metrics import confusion_matrix, f1_score
import numpy
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

stopwords = ['a',
           'about',
           'above',
           'across',
           'after',
           'afterwards',
           'again',
           'against',
           'all',
           'almost',
           'alone',
           'along',
           'already',
           'also',
           'although',
           'always',
           'am',
           'among',
           'amongst',
           'amoungst',
           'amount',
           'an',
           'and',
           'another',
           'any',
           'anyhow',
           'anyone',
           'anything',
           'anyway',
           'anywhere',
           'are',
           'around',
           'as',
           'at',
           'back',
           'be',
           'became',
           'because',
           'become',
           'becomes',
           'becoming',
           'been',
           'before',
           'beforehand',
           'behind',
           'being',
           'below',
           'beside',
           'besides',
           'between',
           'beyond',
           'bill',
           'both',
           'bottom',
           'but',
           'by',
           'call',
           'can',
           'cannot',
           'cant',
           'co',
           'con',
           'could',
           'couldnt',
           'cry',
           'de',
           'describe',
           'detail',
           'do',
           'done',
           'down',
           'due',
           'during',
           'each',
           'eg',
           'eight',
           'either',
           'eleven',
           'else',
           'elsewhere',
           'empty',
           'enough',
           'etc',
           'even',
           'ever',
           'every',
           'everyone',
           'everything',
           'everywhere',
           'except',
           'few',
           'fifteen',
           'fify',
           'fill',
           'find',
           'fire',
           'first',
           'five',
           'for',
           'former',
           'formerly',
           'forty',
           'found',
           'four',
           'from',
           'front',
           'full',
           'further',
           'get',
           'give',
           'go',
           'had',
           'has',
           'hasnt',
           'have',
           'he',
           'hence',
           'her',
           'here',
           'hereafter',
           'hereby',
           'herein',
           'hereupon',
           'hers',
           'herself',
           'him',
           'himself',
           'his',
           'how',
           'however',
           'hundred',
           'i',
           'ie',
           'if',
           'in',
           'inc',
           'indeed',
           'interest',
           'into',
           'is',
           'it',
           'its',
           'itself',
           'keep',
           'last',
           'latter',
           'latterly',
           'least',
           'less',
           'ltd',
           'made',
           'many',
           'may',
           'me',
           'meanwhile',
           'might',
           'mill',
           'mine',
           'more',
           'moreover',
           'most',
           'mostly',
           'move',
           'much',
           'must',
           'my',
           'myself',
           'name',
           'namely',
           'neither',
           'never',
           'nevertheless',
           'next',
           'nine',
           'nobody',
           'none',
           'noone',
           'nor',
           'not',
           'nothing',
           'now',
           'nowhere',
           'of',
           'off',
           'often',
           'on',
           'once',
           'one',
           'only',
           'onto',
           'or',
           'other',
           'others',
           'otherwise',
           'our',
           'ours',
           'ourselves',
           'out',
           'over',
           'own',
           'part',
           'per',
           'perhaps',
           'please',
           'put',
           'rather',
           're',
           'same',
           'see',
           'seem',
           'seemed',
           'seeming',
           'seems',
           'serious',
           'several',
           'she',
           'should',
           'show',
           'side',
           'since',
           'sincere',
           'six',
           'sixty',
           'so',
           'some',
           'somehow',
           'someone',
           'something',
           'sometime',
           'sometimes',
           'somewhere',
           'still',
           'such',
           'system',
           'take',
           'ten',
           'than',
           'that',
           'the',
           'their',
           'them',
           'themselves',
           'then',
           'thence',
           'there',
           'thereafter',
           'thereby',
           'therefore',
           'therein',
           'thereupon',
           'these',
           'they',
           'thick',
           'thin',
           'third',
           'this',
           'those',
           'though',
           'three',
           'through',
           'throughout',
           'thru',
           'thus',
           'to',
           'together',
           'too',
           'top',
           'toward',
           'towards',
           'twelve',
           'twenty',
           'two',
           'un',
           'under',
           'until',
           'up',
           'upon',
           'us',
           'very',
           'via',
           'was',
           'we',
           'well',
           'were',
           'what',
           'whatever',
           'when',
           'whence',
           'whenever',
           'where',
           'whereafter',
           'whereas',
           'whereby',
           'wherein',
           'whereupon',
           'wherever',
           'whether',
           'which',
           'while',
           'whither',
           'who',
           'whoever',
           'whole',
           'whom',
           'whose',
           'why',
           'will',
           'with',
           'within',
           'without',
           'would',
           'yet',
           'you',
           'your',
           'yours',
           'yourself',
           'yourselves']


def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    
    string = re.sub(r"[^A-Za-z0-9(),%!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    string =  string.strip().lower()
    for i in stopwords:
        if i in string:
            string = re.sub(r" (%s) "%i," ",string)
    return string

p = "C:\\Users\\u505123\\Desktop\\Final_Achuth.csv"

tdf = pd.read_csv(p)
df = tdf[0:int(0.7*len(tdf))]
yesdf = pd.DataFrame(df["Phrase"].loc[df['Indicator'] == "Yes"],columns=["Phrase","Class"])
nodf = pd.DataFrame(df["Phrase"].loc[df['Indicator'] == "No"],columns=["Phrase","Class"])
yesdf.index = [i for i in range(0,len(yesdf.index))]
nodf.index = [i for i in range(0,len(nodf.index))]
yesdf["Class"] = [1 for i in range(0,len(yesdf.index))]
nodf["Class"] = [0 for i in range(0,len(nodf.index))]

data = yesdf.append(nodf)
data.index = [i for i in range(0,len(data.index))]

final_phrase_list = []
for i in data["Phrase"]:
    x = clean_str(i)
    final_phrase_list.append(x)
data["Phrase"] = [i for i in final_phrase_list]

data = data.reindex(numpy.random.permutation(data.index))
count_vectorizer = CountVectorizer()
sample = count_vectorizer.fit_transform(data['Phrase'].values)
features = TfidfVectorizer(data['Phrase'])
X = [sample,features]
Y = [i for i in data["Class"]]
clf = MLPClassifier(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
'''

counts = count_vectorizer.fit_transform(data['Phrase'].values)

classifier = MultinomialNB()
targets = data['Class'].values
classifier.fit(counts, targets)

example = ["Customer A accounted for 15% of net sales.", "Major contribution from the geographical area was from Venezuela"]

example_counts = count_vectorizer.transform(example)
predictions = classifier.predict(example_counts)
predictions
'''
#example = ["Customer A accounted for 15% of net sales.", "Major contribution from the geographical area was from Venezuela"]

example = []
test_df = tdf[int(0.7*len(tdf)):]
for i in test_df["Phrase"]:
    if i != "Phrase":
        x = clean_str(i)
        example.append(x)


pipeline = Pipeline([
    ('vectorizer',  CountVectorizer()),
    ('classifier',  MultinomialNB()) ])

pipeline.fit(data['Phrase'].values, data['Class'].values)
ans = pipeline.predict(example)

j=0
prec_count = 0
for i in test_df["Indicator"]:
    if i=="Indicator":
        continue
    if i=="Yes" and ans[j]==1:
        prec_count+=1
    j+=1
'''
k_fold = KFold(n=len(data), n_folds=6)
scores = []
confusion = numpy.array([[0, 0], [0, 0]])
for train_indices, test_indices in k_fold:
    train_text = data.iloc[train_indices]['Phrase'].values
    train_y = data.iloc[train_indices]['Class'].values

    test_text = data.iloc[test_indices]['Phrase'].values
    test_y = data.iloc[test_indices]['Class'].values

    pipeline.fit(train_text, train_y)
    predictions = pipeline.predict(test_text)

    confusion += confusion_matrix(test_y, predictions)
    score = f1_score(test_y, predictions, pos_label=1)
    scores.append(score)

print('Total emails classified:', len(data))
print('Score:', sum(scores)/len(scores))
print('Confusion matrix:')
print(confusion)
'''