import nltk
from nltk.corpus import wordnet as wn
import gensim
from gensim import corpora
import pickle

def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma
    
from nltk.stem.wordnet import WordNetLemmatizer
def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

en_stop = set(nltk.corpus.stopwords.words('english'))

import spacy
from spacy.lang.en import English
parser = English()

def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens

def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

def lda(path):
    text_data = []
    with open('c1.txt') as f:
        for line in f:
            tokens = prepare_text_for_lda(line)
            text_data.append(tokens)
                
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    NUM_TOPICS = 5
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=20)
    ldamodel.save('model3.gensim')
    topics = ldamodel.print_topics(num_words=5)
   # for topic in topics:
    #    print(topic)
    file = open(path, 'r')
    read_file = file.read()
    new_doc = prepare_text_for_lda(read_file)
    new_doc_bow = dictionary.doc2bow(new_doc)
    tmp = ldamodel.get_document_topics(new_doc_bow)
    return tmp

