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

