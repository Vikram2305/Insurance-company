# -*- coding: utf-8 -*-
"""R ass.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kZiC8_L4nPggOU_urWKiJsiqVvAAcduY
"""

from bs4 import BeautifulSoup as bs
import requests 
import pandas as pd
import matplotlib.pyplot as plt 

urls=["https://groww.in/blog/top-life-insurance-companies-in-india","https://www.policybazaar.com/insurance-companies/"]
headers_={'user-agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)'}

for url in urls:
  page=requests.get(url, headers=headers_)

  soup=bs(page.content,'html.parser')

  Contents=soup.findAll("p")

Scrapped_data=[]
for content in Contents:
  Text=content.get_text()
  Scrapped_data.append([Text])

df=pd.DataFrame(Scrapped_data,columns=["Text"])

display(df)

df.to_json("ins_company.json")

import string
string.punctuation
def remove_punctuation(text):
    punctuationfree="".join([i for i in text if i not in string.punctuation])
    return punctuationfree
#storing the puntuation free text
df['puntuation free text']= df['Text'].apply(lambda x:remove_punctuation(x))
#Lowering the text
df['lower']= df['puntuation free text'].apply(lambda x: x.lower())

#Tokenization
from nltk.tokenize import TweetTokenizer as tt
#applying function to the column
tokenizer = tt()      
df['tokenized_text'] = df['lower'].apply(lambda x: tokenizer.tokenize(x))

#Removing stop words
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
stopword = stopwords.words('english')
def remove_stopwords(text):
    output= [i for i in text if i not in stopword]
    return output
df['no_stopwords']= df['tokenized_text'].apply(lambda x:remove_stopwords(x))

#Stemming 
from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()
#Defining a function for stemming
def stemming(text):
    stem_tweet = [porter_stemmer.stem(word) for word in text]
    return stem_tweet
df['stemmed_text']=df['no_stopwords'].apply(lambda x: stemming(x))

#Lemmatization
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
nltk.download('omw-1.4')
wordnet_lemmatizer = WordNetLemmatizer()
def lemmatizer(stemmed_books):
    lemm_text = [wordnet_lemmatizer.lemmatize(word) for word in stemmed_books]
    return lemm_text
df['lemmatized_text']=df['stemmed_text'].apply(lambda x:lemmatizer(x))
display(df.head())

!pip install pyLDAvis

import numpy as np
import json
import glob

#Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

#spacy
import spacy
import nltk
from nltk.corpus import stopwords

#Vis
import pyLDAvis
import pyLDAvis.gensim

import warnings 
warnings.filterwarnings("ignore",category=DeprecationWarning)

def load_data(file):
  with open(file,"r",encoding="utf-8") as f:
    data=json.load(f)
  return(data)

def write_data(file,data):
  with open(file,"w",encoding="utf-8") as f:
    json.dump(data,f,indent=4)

nltk.download("stopwords")
print(stopwords)

data=load_data("/content/ins_company.json")["Text"]
data=data["50"]
data=data.split(".")
data

def lemmatization(texts,allowed_postages=["NOUN","ADJ","VERB","ADV"]):
  nlp=spacy.load("en_core_web_sm",disable=["senter","ner","parser"])
  texts_out=[]
  for text in texts:
    doc=nlp(text)
    new_text=[]
    for token in doc:
      if token.pos_ in allowed_postages:
        new_text.append(token.lemma_)
    final=" ".join(new_text)
    texts_out.append(final)
  return (texts_out)

lemmatized_texts=lemmatization(data)
lemmatized_texts

def gen_words(texts):
  final=[]
  for text in texts:
    new=gensim.utils.simple_preprocess(text,deacc=True)
    final.append(new)
  return(final)

data_words=gen_words(lemmatized_texts)
print(data_words)

id2word=corpora.Dictionary(data_words)
corpus=[]
for text in data_words:
  new = id2word.doc2bow(text)
  corpus.append(new)

print(corpus)

word = id2word
print(word)

lda_model= gensim.models.ldamodel.LdaModel(corpus=corpus,id2word=id2word,num_topics=30,random_state=100,update_every=1,
                                           chunksize=100,passes=10,alpha="auto")

pyLDAvis.enable_notebook()
vis=pyLDAvis.gensim.prepare(lda_model,corpus,id2word,mds="mmds",R=30)
vis

