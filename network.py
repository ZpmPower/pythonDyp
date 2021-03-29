# Import required libraries
import pandas as pd
import numpy as np 
import sklearn
from plotCategoryCount import drawCategoryCountPlot

# Import necessary modules
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing
from math import sqrt

# Keras specific
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical 
from keras.utils import np_utils
from keras.wrappers.scikit_learn import KerasClassifier


def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(8, input_dim=26, activation='relu'))
	model.add(Dense(7, activation='softmax'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

dataframe = pd.read_csv('baza.csv') 
columbs = ["data_channel_is_lifestyle", "data_channel_is_entertainment", "data_channel_is_bus", "data_channel_is_socmed", "data_channel_is_tech", "data_channel_is_world", "data_channel_is_other"]
dataset = dataframe.values
X = dataset[:,0:26].astype(float)
Y = dataset[:,26:33]

testY = dataframe[["data_channel_is_lifestyle", "data_channel_is_entertainment", "data_channel_is_bus", "data_channel_is_socmed", "data_channel_is_tech", "data_channel_is_world", "data_channel_is_other"]]
categories = list(testY.columns)
cat_count = [] 
x = 0;
for c in columbs:
    cat_count.append(testY[c].value_counts()[1])
    x+=testY[c].value_counts()[1]

#DrawPlot
#drawCategoryCountPlot(categories,cat_count)

x_train, x_test, y_train, y_test = train_test_split(X, Y , train_size = 0.7, random_state =  90)
print(X)
print("HUY")
std_scale = preprocessing.StandardScaler().fit(X)
x_norm = std_scale.transform(X)
print(x_norm)

estimator = KerasClassifier(build_fn=baseline_model, epochs=50, batch_size=250, verbose=0)
kfold = KFold(n_splits=10, shuffle=True)
results = cross_val_score(estimator, x_norm, Y, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))	 	 	 	
