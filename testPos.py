import nltk
nltk.download('stopwords')
nltk.download('punkt')
import re
import tkinter
import string
import gensim
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.scrolledtext as tkst
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
from collections import Counter
from textblob import TextBlob
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from lda import lda
from rake_nltk import Rake

def MinMaxPolarities(title):
    pos_word_list=[]
    neu_word_list=[]
    neg_word_list=[]
    pos_word_count =0
    neu_word_count = 0
    neg_word_count = 0
    min_pos = 1
    max_pos = 0
    avg_pos = 0
    
    min_neg = 0
    max_neg = -1
    avg_neg = 0
    
    rate_pos = 0
    rate_neg = 0
    count = 0
    for word in title:               
        testimonial = TextBlob(word)
        if testimonial.sentiment.polarity > 0:
            if(min_pos > testimonial.sentiment.polarity):
                min_pos = testimonial.sentiment.polarity
            if(max_pos < testimonial.sentiment.polarity):
                max_pos = testimonial.sentiment.polarity
            pos_word_list.append(word)
            avg_pos = avg_pos + testimonial.sentiment.polarity
            pos_word_count  = pos_word_count + 1
        elif testimonial.sentiment.polarity < 0:
            neg_word_list.append(word)
            if(min_neg > testimonial.sentiment.polarity):
                min_neg = testimonial.sentiment.polarity
            if(max_neg < testimonial.sentiment.polarity):
                max_neg = testimonial.sentiment.polarity
            avg_neg = avg_neg + testimonial.sentiment.polarity
            neg_word_count =neg_word_count + 1
        else:
            neu_word_list.append(word)
            neu_word_count = neu_word_count+1
        count = count + 1

    print('Positive :',pos_word_list)        
    print('Neutral :',neu_word_list)    
    print('Negative :',neg_word_list) 
    
    if not pos_word_list:
        min_pos = 0
        max_pos = 0
        avg_pos = 0
    else:
        avg_pos = avg_pos/pos_word_count
        
#    print('Positive min :',min_pos)  
#    print('Positive max :',max_pos)
#    print('Positive avg :',avg_pos)
#    for x in pos_word_list:
#        print(x + ' polarity =' + str(TextBlob(x).sentiment.polarity))
        
    if not neg_word_list:
        min_neg = 0
        max_neg = 0
        avg_neg = 0
    else:
        avg_neg = avg_neg/neg_word_count
        
#    print('Negative min :',min_neg)  
#    print('Negative max :',max_neg)
#    print('Negative avg :',avg_neg)
#    for x in neg_word_list:
#        print(x + ' polarity =' + str(TextBlob(x).sentiment.polarity))
    if(neg_word_count == 0):
        rate_neg = 0
        rate_pos = 1    
    elif(pos_word_count == 0):
        rate_neg = 1
        rate_pos = 0
    else:
        rate_pos = pos_word_count / (pos_word_count + neg_word_count)
        rate_neg = 1 - rate_pos
    
    global_rate_pos = pos_word_count/count
    global_rate_neg = neg_word_count/count
#    print('Global pos = ' + str(global_rate_pos))
#    print('Global neg = ' + str(global_rate_neg))
    return global_rate_pos, global_rate_neg,rate_pos, rate_neg, avg_pos,min_pos,max_pos,avg_neg,min_neg,max_neg