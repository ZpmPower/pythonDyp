import nltk
nltk.download('stopwords')
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
#from lda import lda
from rake_nltk import Rake


def countWords(string):
    return len(string)

def uniqueWords(string):
    return list(Counter(string))

def countUnique(string):
    return len(Counter(string)) 

def nonStopWords(string):
   stop_words = set(stopwords.words('english'))
   # words = word_tokenize(" ".join(string))
   nonstopText = []
   for word in string:
       if word not in stop_words:
           nonstopText.append(word)
           return nonstopText

def nonStopCount(string):
    return countWords(nonStopWords(string))

def averageWordLength(string):
    return sum(len(word) for word in string) / len(string)

def sentiment_textblob(feedback): 
    senti = TextBlob(feedback) 
    polarity = senti.sentiment.polarity   
    return polarity

def sentiment_analyzer_scores(sentence):
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))

def num_keyword(title):
    meta = str(textMeta.get("1.0",'end-1c'))
    metaRes = [word.strip(string.punctuation) for word in meta.split()]
#print(countWords(metaRes))
    r = Rake() # Uses stopwords for english from NLTK, and all puntuation characters.
    r.extract_keywords_from_text(title)
#print(r.get_ranked_phrases()) # To get keyword phrases ranked highest to lowest.
    result = len(r.get_ranked_phrases())  + countWords(metaRes) -1
    return result

def subjectivity(string):
    return TextBlob(string).subjectivity

def abs_title_subjectivity(subject):
    value = float(subject)
    if value == 0:
        value = 0.5
        return value
    if value >=  0.5:
        value = value - 0.5
        return value
    if value > 0 and value < 0.5:
        value = 0.5 - value
        return value

def resultBtn_click():
    resultText.delete('1.0', END)
    
    images = comboImages.get()
    videos = comboVideos.get()
    links = comboLinks.get()
    if (comboDay.get()=="No"):
        day = 0
    elif comboDay.get()=="Yes":
        day = 1
    
   # thmz = text.get("1.0",END)
    
    file_content = str(textContent.get("1.0",'end-1c'))
    content = [word.strip(string.punctuation) for word in file_content.split()]
    while("" in content) : 
        content.remove("")

    file_title = str(textTitle.get("1.0",'end-1c'))
    title = [word.strip(string.punctuation) for word in file_title.split()]
    while("" in title) : 
        title.remove("")

    numLinks = 5 #Number of Links
    numVideos = 0 #Number of Videos
    numImages = 2 #Number of Images

    countwordsT = countWords(title) #Number of Words Title

    countwordsC = countWords(content) #Number of Words Content
##
    countunique = countUnique(content) #Number of Unique Words

    nonstopCount = nonStopCount(content) # Number of non-Stop Words
    #print(nonstopCount)

    rateNonStopWords = 0.999999995192
# Rate of non-Stop Words
#
    rateUniqueNonStopWords = nonStopCount(uniqueWords(content))/nonstopCount # Rate of Unique non-Stop Words

    average_token_length = averageWordLength(content) # Average Words Length

    global_subjectivity = TextBlob(' '.join(content)).subjectivity
    title_subjectivity = TextBlob(' '.join(title)).subjectivity
    global_sentiment_polarity = TextBlob(' '.join(content)).polarity 
    title_sentiment_polarity = TextBlob(' '.join(title)).polarity
    #LDA = lda('content.txt')

    print('n_tokens_title =',countwordsT)
    print('n_tokens_content =',countwordsC)

    print('n_unique_tokens =',countunique)
    print('n_non_stop_words =',rateNonStopWords)
    print('n_non_stop_unique_tokens =',rateUniqueNonStopWords)

    print('num_href =',numLinks)
    print('num_imgs =',numImages)
    print('num_videos =',numVideos)
    print('average_token_length =',average_token_length)

    num_keywords=num_keyword(" ".join(title))
    print('num_keywords =', num_keywords)

    is_workday = 1
    is_weekend = 0
    print('is_workday=', is_workday)
    print('is_weekend=', is_weekend)


#    print('LDA00 =',LDA[0][1])
#    print('LDA01 =',LDA[1][1])
#    print('LDA02 =',LDA[2][1])
#    print('LDA03 =',LDA[3][1])
#    print('LDA04 =',LDA[4][1])

    print('global_subjectivity =',global_subjectivity)
    print('global_sentiment_polarity=', global_sentiment_polarity)

    avg_positive_polarity = 0.35
    min_positive_polarity = 0.1
    max_positive_polarity = 0.75
    abs_title_sub= abs_title_subjectivity(title_subjectivity)
    abs_title_sentiment_polarity = abs(title_sentiment_polarity)
    print('avg_positive_polarity=',avg_positive_polarity)
    print('min_positive_polarity=',min_positive_polarity)
    print('max_positive_polarity=',max_positive_polarity)
    print('title_subjectivity=',title_subjectivity)
    print('title_sentiment_polarity=',title_sentiment_polarity)
    print('abs_title_subjectivity=',abs_title_sub)
    print('abs_title_sentiment_polarity=',abs_title_sentiment_polarity)

    result = str(countwordsT) + ' ' + str(countwordsC) + ' ' + str(countunique/countwordsC) + ' ' + str(rateNonStopWords) + ' ' + str(rateUniqueNonStopWords) + ' ' + str(links) + ' ' + str(videos) + ' ' + str(images) + ' ' + str(average_token_length) + ' ' + str(num_keywords) + ' ' + str(is_workday) + ' ' + str(is_weekend)+ ' ' + str(global_subjectivity) + ' ' + str(global_sentiment_polarity) + ' ' + str(avg_positive_polarity) + ' ' + str(min_positive_polarity) + ' ' + str(max_positive_polarity) + ' ' + str(title_subjectivity) +' ' + str(title_sentiment_polarity) + ' ' + str(abs_title_sub) + ' ' + str(abs_title_sentiment_polarity) 
 #   + str(LDA[0][1]) + ' '  + str(LDA[1][1]) + ' ' + str(LDA[2][1]) + ' ' + str(LDA[3][1]) + ' ' + str(LDA[4][1]) + ' ' 
    
    resultText.insert(END,result)

root = Tk()
root.title("Analyzer")
root.geometry("500x450")
root.resizable(False, False)

labelTitle = tkinter.Label(root,text = "Title:")
labelTitle.place(x=8,y=5)
#textTitle = StringVar()
#textTitle_entry = Entry(textvariable=textTitle)
#textTitle_entry.place(x=10,y=25, relwidth=0.96, height=34)
textTitle = tkst.ScrolledText()
textTitle.place(x=10,y=25, relwidth=0.96, height=34)

labelContent = tkinter.Label(root, text = "Content:")
labelContent.place(x=8,y=60)
#textContent = StringVar()
#textContent_entry = Entry(textvariable=textContent)
#textContent_entry.place(x=10,y=80, relwidth=0.96, height=105)
textContent = tkst.ScrolledText()
textContent.place(x=10,y=80, relwidth=0.96, height=105)
#
labelLinks = tkinter.Label(root, text = "Number of Links:")
labelLinks.place(x=8,y=185)
comboLinks = ttk.Combobox(root)
comboLinks['values']= ("0","1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "100", 
"101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "140", "141", "142", "143", "144", "145", "146", "147", "148", "149", "150", "151", "152", "153", "154", "155", "156", "157", "158", "159", "160", "161", "162", "163", "164", "165", "166", "167", "168", "169", "170", "171", "172", "173", "174", "175", "176", "177", "178", "179", "180", "181", "182", "183", "184", "185", "186", "187", "188", "189", "190", "191", "192", "193", "194", "195", "196", "197", "198", "199", "200", 
"201", "202", "203", "204", "205", "206", "207", "208", "209", "210", "211", "212", "213", "214", "215", "216", "217", "218", "219", "220", "221", "222", "223", "224", "225", "226", "227", "228", "229", "230", "231", "232", "233", "234", "235", "236", "237", "238", "239", "240", "241", "242", "243", "244", "245", "246", "247", "248", "249", "250", "251", "252", "253", "254", "255", "256", "257", "258", "259", "260", "261", "262", "263", "264", "265", "266", "267", "268", "269", "270", "271", "272", "273", "274", "275", "276", "277", "278", "279", "280", "281", "282", "283", "284", "285", "286", "287", "288", "289", "290", "291", "292", "293", "294", "295", "296", "297", "298", "299", "300")
comboLinks.place(x=10,y=205, relwidth = 0.25)
comboLinks.current(0)
#
labelVideos = tkinter.Label(root, text = "Number of Videos:")
labelVideos.place(x=188,y=185)
comboVideos = ttk.Combobox(root)
comboVideos['values']= ("0","1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90")
comboVideos.place(x=190,y=205, relwidth = 0.25)
comboVideos.current(0)
#
labelImages = tkinter.Label(root, text = "Number of Images:")
labelImages.place(x=363,y=185)
comboImages = ttk.Combobox(root)
comboImages['values']= ("0","1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "100", 
"101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120")
comboImages.place(x=365,y=205, relwidth = 0.25)
comboImages.current(0)
#

labelTitle = tkinter.Label(root,text = "MetaData:")
labelTitle.place(x=28,y=230)
textMeta = tkst.ScrolledText()
textMeta.place(x=30,y=250, relwidth=0.3, height=40)

labelDay = tkinter.Label(root, text = "Is published in the working day?")
labelDay.place(x=180,y=240)
comboDay = ttk.Combobox(root)
comboDay['values']= ("No","Yes")
comboDay.place(x=190,y=260)
comboDay.current(0)
#
resultBtn = Button(text="Activate", command=lambda: resultBtn_click(), height=2, width = 10)
resultBtn.place(x=380, y=250) 
#
label12 = tkinter.Label(root, text = "Result:")
label12.place(x=228, y=303)
#
#result = StringVar()
#result_entry = Entry(textvariable=result)
#result_entry.place(x=10,y=325, relwidth=0.96, relheight=0.17)
resultText = tkst.ScrolledText()
resultText.place(x=10,y=325, relwidth=0.96, relheight=0.25)

#file = open('content.txt', 'r')
#read_file = file.read()
#
#file1 = open('title.txt', 'r')
#read_file1 = file1.read() 
#
#file_content = str(read_file)
#content = [word.strip(string.punctuation) for word in file_content.split()]
#while("" in content) : 
#    content.remove("")
#
#file_title = str(read_file1)
#title = [word.strip(string.punctuation) for word in file_title.split()]
#while("" in title) : 
#    title.remove("")
#
#numLinks = 5 #Number of Links
#numVideos = 0 #Number of Videos
#numImages = 2 #Number of Images
#
#countwordsT = countWords(title) #Number of Words Title
#
#countwordsC = countWords(content) #Number of Words Content
###
#countunique = countUnique(content) #Number of Unique Words
#
#nonstopCount = nonStopCount(content) # Number of non-Stop Words
##print(nonstopCount)
#
#rateNonStopWords = 0.999999995192
## Rate of non-Stop Words
##
#rateUniqueNonStopWords = nonStopCount(uniqueWords(content))/nonstopCount # Rate of Unique non-Stop Words
#
#average_token_length = averageWordLength(content) # Average Words Length
#
#global_subjectivity = TextBlob(' '.join(content)).subjectivity
#title_subjectivity = TextBlob(' '.join(title)).subjectivity
#global_sentiment_polarity = TextBlob(' '.join(content)).polarity 
#title_sentiment_polarity = TextBlob(' '.join(title)).polarity
#LDA = lda('content.txt')
#
#print('n_tokens_title =',countwordsT)
#print('n_tokens_content =',countwordsC)
#
#print('n_unique_tokens =',countunique)
#print('n_non_stop_words =',rateNonStopWords)
#print('n_non_stop_unique_tokens =',rateUniqueNonStopWords)
#
#print('num_href =',numLinks)
#print('num_imgs =',numImages)
#print('num_videos =',numVideos)
#print('average_token_length =',average_token_length)
#
#num_keywords=num_keyword(" ".join(title))
#print('num_keywords =', num_keywords)
#
#is_workday = 1
#is_weekend = 0
#print('is_workday=', is_workday)
#print('is_weekend=', is_weekend)
#
#
#print('LDA00 =',LDA[0][1])
#print('LDA01 =',LDA[1][1])
#print('LDA02 =',LDA[2][1])
#print('LDA03 =',LDA[3][1])
#print('LDA04 =',LDA[4][1])
#
#print('global_subjectivity =',global_subjectivity)
#print('global_sentiment_polarity=', global_sentiment_polarity)
#
#avg_positive_polarity = 0.35
#min_positive_polarity = 0.1
#max_positive_polarity = 0.75
#abs_title_subjectivity= abs_title_subjectivity(title_subjectivity)
#abs_title_sentiment_polarity = abs(title_sentiment_polarity)
#print('avg_positive_polarity=',avg_positive_polarity)
#print('min_positive_polarity=',min_positive_polarity)
#print('max_positive_polarity=',max_positive_polarity)
#print('title_subjectivity=',title_subjectivity)
#print('title_sentiment_polarity=',title_sentiment_polarity)
#print('abs_title_subjectivity=',abs_title_subjectivity)
#print('abs_title_sentiment_polarity=',abs_title_sentiment_polarity)
#
#result = str(countwordsT) + ' ' + str(countwordsC) + ' ' + str(countunique) + ' ' + str(rateNonStopWords) + ' ' + str(rateUniqueNonStopWords) + ' ' + str(numLinks) + ' ' + str(numVideos) + ' ' + str(numImages) + ' ' + str(average_token_length) + ' ' + str(num_keywords) + ' ' + str(is_workday) + ' ' + str(is_weekend)+ ' ' + str(LDA[0][1]) + ' ' + str(LDA[1][1]) + ' ' + str(LDA[2][1]) + ' ' + str(LDA[3][1]) + ' ' + str(LDA[4][1]) + ' ' + str(global_subjectivity) + ' ' + str(global_sentiment_polarity) + ' ' + str(avg_positive_polarity) + ' ' + str(min_positive_polarity) + ' ' + str(max_positive_polarity) + ' ' + str(title_subjectivity) +' ' + str(title_sentiment_polarity) + ' ' + str(abs_title_subjectivity) + ' ' + str(abs_title_sentiment_polarity) 
#f = open("result.txt", "w")
#f.write(result)
#f.close()

root.mainloop()



