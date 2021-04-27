import pandas as pd
from keras.models import model_from_json
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

def load_model(name):
    model_name = "model" + name
    # load json and create model
    json_file = open(model_name + ".json", 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(model_name + ".h5")
    print("Loaded model from disk")

    return loaded_model

dataframe = pd.read_csv('bazaSelfRef.csv') 
dataset = dataframe.values
X = dataset[:,0:32].astype(float)
Y = dataset[:,32:38]
model = load_model("1")


std_scale = preprocessing.StandardScaler().fit(X)
X_std = std_scale.transform(X)
x_train, x_test, y_train, y_test = train_test_split(X_std, Y , train_size = 0.9, random_state =  90)

Y_test = np.argmax(y_test, axis=1) # Convert one-hot to index
y_pred = model.predict_classes(x_test)
print(classification_report(Y_test, y_pred))
#print(len(y_pred))
count_cool = 0
for i in range(3847):
    if y_pred[i]==Y_test[i]:
        count_cool+=1
print("Good:" + str(count_cool))
print("All:" + str(len(Y_test)))
print("test: " + str(count_cool / len(Y_test)))


