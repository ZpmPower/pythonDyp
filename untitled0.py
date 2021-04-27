# Import required libraries
import pandas as pd
import numpy as np 
import sklearn
from numpy import array
from plotCategoryCount import drawCategoryCountPlot

# Import necessary modules
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing
from math import sqrt
from matplotlib import pyplot
# Keras specific
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Convolution1D, BatchNormalization, Flatten, \
    MaxPooling1D
from keras.utils import to_categorical 
from keras.utils import np_utils
from keras.wrappers.scikit_learn import KerasClassifier
from keras.models import model_from_json
from keras.callbacks import TensorBoard  
from keras.optimizers import SGD


dataframe = pd.read_csv('baza.csv') 
columnsToNormalise = ['n_tokens_title','n_tokens_content','num_hrefs','num_imgs','num_videos','average_token_length','num_keywords','global_sentiment_polarity','title_sentiment_polarity']
dataframe[columnsToNormalise] = preprocessing.MinMaxScaler().fit_transform(dataframe[columnsToNormalise])
columbs = ["data_channel_is_lifestyle", "data_channel_is_entertainment", "data_channel_is_bus", "data_channel_is_socmed", "data_channel_is_tech", "data_channel_is_world", "data_channel_is_other"]
dataset = dataframe.values
X = dataset[:,0:26].astype(float)
Y = dataset[:,26:33]

def fit_model(trainX, trainy, testX, testy, lrate):
	# define model
	model = Sequential()
	model.add(Dense(15, input_dim=len(X[0]), activation='sigmoid'))
	model.add(Dense(50, activation='sigmoid'))
	model.add(Dense(250, activation='sigmoid'))
	model.add(Dense(250, activation='sigmoid'))
	model.add(Dense(250, activation='sigmoid'))
	model.add(Dense(len(Y[0])))
	model.add(Activation('softmax'))
	# compile model
	opt = keras.optimizers.Adam(lr=lrate)
	model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
	# fit model
	history = model.fit(trainX, trainy, validation_data=(testX, testy), epochs=100,batch_size=100, verbose=1)
	# plot learning curves
	pyplot.plot(history.history['acc'], label='train')
	pyplot.plot(history.history['val_acc'], label='test')
	pyplot.title('lrate='+str(lrate), pad=-50)


x_train, x_test, y_train, y_test = train_test_split(X, Y , train_size = 0.8, random_state =  90)

# create learning curves for different learning rates
learning_rates = [1E-0, 1E-1, 1E-2, 1E-3]
for i in range(len(learning_rates)):
	# determine the plot number
	plot_no = 420 + (i+1)
	pyplot.subplot(plot_no)
	# fit model and plot learning curves for a learning rate
	fit_model(x_train, y_train, x_test, y_test, learning_rates[i])
# show learning curves
pyplot.show()