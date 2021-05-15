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
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedShuffleSplit
from math import sqrt
from matplotlib import pyplot
# Keras specific
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Convolution1D, BatchNormalization, Flatten, Dropout 
from keras.utils import to_categorical 
from keras.utils import np_utils
from keras.wrappers.scikit_learn import KerasClassifier
from keras.models import model_from_json
from keras.callbacks import TensorBoard, ModelCheckpoint

def load_data(name):
    dataframe = pd.read_csv(name +'.csv') 
#columnsToNormalise = ['n_tokens_title','n_tokens_content','num_hrefs','num_imgs','num_videos','average_token_length','num_keywords','global_sentiment_polarity','title_sentiment_polarity']
#dataframe[columnsToNormalise] = preprocessing.StandardScaler().fit_transform(dataframe[columnsToNormalise])
    columbs = ["data_channel_is_lifestyle", "data_channel_is_entertainment", "data_channel_is_bus", "data_channel_is_socmed", "data_channel_is_tech", "data_channel_is_world", "data_channel_is_other"]
    dataset = dataframe.values
    X = dataset[:,0:40].astype(float)
    Y = dataset[:,40:47]
    dataframe.to_csv('./output/outputStandart.csv', index = False, header=True)
    return X,Y,dataframe,columbs
    
def create_model():
	# create model
  model = Sequential()
  model.add(Dense(50, input_dim=len(X[0]), activation = 'elu'))
  model.add(Dropout(0.2))
  model.add(Dense(100, activation='elu'))
  model.add(Dropout(0.2))
  model.add(BatchNormalization())
  model.add(Dense(100, activation='elu'))
  model.add(Dense(100, activation='elu'))
  model.add(Dense(100, activation='elu'))
  model.add(Dense(len(Y[0])))
  model.add(Activation('softmax'))
  # Compile model
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  print(model.summary())
  return model


def save_model(model,name):
	# serialize model to JSON
	model_json = model.to_json()
	with open("model" + name + ".json", "w") as json_file:
   		json_file.write(model_json)
	# serialize weights to HDF5
	model.save_weights("model" + name + ".h5")
	print("Saved model to disk")

def load_model(name):
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")


X,Y,dataframe,columbs = load_data('baza')
testY = dataframe[["data_channel_is_lifestyle", "data_channel_is_entertainment", "data_channel_is_bus", "data_channel_is_socmed", "data_channel_is_tech", "data_channel_is_world", "data_channel_is_other"]]
categories = list(testY.columns)
cat_count = [] 
x = 0;
for c in columbs:
    cat_count.append(testY[c].value_counts()[1])
    x+=testY[c].value_counts()[1]

#DrawPlot
#drawCategoryCountPlot(categories,cat_count)

#####################################################
##SCALERS
#minmax_scale = preprocessing.MinMaxScaler().fit(X)
##nrm_scale = preprocessing.normalize().fit(x_train,norm='l2')
#######################################################
#######################################################
## SCALERED DATA
#x_train_std = std_scale.transform(x_train)
#x_minmax = minmax_scale.transform(X)
#x_nrm = preprocessing.normalize(x_train,norm='l2')
#######################################################

std_scale = preprocessing.StandardScaler().fit(X)
X_std = std_scale.transform(X)

x_train, x_test, y_train, y_test = train_test_split(X_std, Y , train_size = 0.90, random_state =  90)

model = create_model()
# checkpoint
filepath="./weight/weights-improvement-{epoch:02d}-{val_acc:.2f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]

history = model.fit(x_train, y_train, epochs=100, batch_size=1000, verbose=1, validation_data=(x_test, y_test))

# plot learning curves
pyplot.plot(history.history['acc'], label='train')
pyplot.plot(history.history['val_acc'], label='test')
pyplot.show()
save_model(model,"1")
#estimator = KerasClassifier(build_fn=create_model, epochs=250, batch_size=5000, verbose=1)
#kfold = KFold(n_splits=10, shuffle=True)
#results = cross_val_score(estimator, x_std, Y, cv=kfold)
#print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))	 	
#Xnew = array([[0.476190476,0.023770104,0.663594467,0.999999992,0.815384609,0.013157895,0.0078125,0,0.243241503,0.444444444,1	,0	,0	,0	,0,	0	,0	,0,	0.521617145	,0.433591231,	0.1,	0.7,	0.5,	0.40625,	0,	0.1875]])
#Xnew_std = minmax_scale.transform(Xnew)
#ynew = model.predict_classes(Xnew_std)
# show the inputs and predicted outputs

#print("X=%s, Predicted=%s" % (Xnew[0], ynew[0]))