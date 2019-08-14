"""

"""

#%%

import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

from tensorflow.python import keras
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Flatten, Conv2D, Dropout

#%%
def data_preprocess(x_train, y_train, x_test, y_test, param):
    
    # Converts a class vector (integers) to binary class matrix.  
    y_train_out = tf.keras.utils.to_categorical(y_train,param['num_classes'],dtype='uint8')
    y_test_out = tf.keras.utils.to_categorical(y_test,param['num_classes'],dtype='uint8')
    
    # Normalize data
    x_train_out =  x_train / 255
    x_test_out =  x_test / 255
    
    # Reshape data to 4 dimensions
    x_train_out = x_train_out.reshape(param['num_images_train'], param['img_rows'], param['img_cols'], 1)
    x_test_out = x_test_out.reshape(param['num_images_test'], param['img_rows'], param['img_cols'], 1)
    
    return (x_train_out, y_train_out), (x_test_out, y_test_out)

#%%
def data_posprocess(prediction,top):
    
    prediction_out = np.zeros((prediction.shape[0],top)).astype(int)
    
    for pred in range(len(prediction)):
        prediction_out[pred,:] = prediction[pred].argsort()[-top:][::-1]
    
    return prediction_out

#%%
def data_show(prediction,y_labels,nimages):
    
    
    fashion_mnist_labels = ["T-shirt/top",  # index 0
                            "Trouser",      # index 1
                            "Pullover",     # index 2 
                            "Dress",        # index 3 
                            "Coat",         # index 4
                            "Sandal",       # index 5
                            "Shirt",        # index 6 
                            "Sneaker",      # index 7 
                            "Bag",          # index 8 
                            "Ankle boot"]   # index 9
    
    nrandom = np.random.choice(prediction.shape[0],nimages)
    
    figure = plt.figure(figsize=(14, 6))
    
    for i, index in enumerate(nrandom):
        subplot = figure.add_subplot(3, 5, i + 1, xticks=[], yticks=[])
        
        predict_index = prediction[index][0]
        true_index = np.argmax(y_test[index])
        subplot.imshow(np.squeeze(x_test[index])) 
        subplot.set_title("{}".format(fashion_mnist_labels[predict_index]), 
                    color=("green" if predict_index == true_index else "red"))
    
    return 
    
#%% **************************** Main Code ************************************

(x_train, y_train), (x_test, y_test) = keras.datasets.fashion_mnist.load_data()


# Create a dictionary with general parameters
param = {'num_classes': len(np.unique(y_train)),
         'img_rows': x_train.shape[1],
         'img_cols': x_train.shape[2],
         'num_images_train': x_train.shape[0],
         'num_images_test': x_test.shape[0]
         }

# Pre-process function
(x_train, y_train), (x_test, y_test) = data_preprocess(x_train,y_train,x_test,y_test,param)

#%%

# Create the network structure
model = Sequential()
model.add(Conv2D(20, kernel_size=(3, 3),
                 strides=1,
                 activation='relu',
                 input_shape=(param['img_rows'], param['img_cols'], 1)))
model.add(Dropout(0.5))
model.add(Conv2D(20, kernel_size=(3, 3),
                 strides=1,
                 activation='relu'))
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(param['num_classes'], activation='softmax'))

# Compile it
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer='adam',
              metrics=['accuracy'])

# Training process
model.fit(x_train, y_train,
          batch_size=128,
          epochs=2,
          validation_split = 0.2)


# Make the preditions
preds = model.predict(x_test)

# Pos-process function
preds = data_posprocess(preds,top=1)

# Show some predicted labels
data_show(preds, y_test, nimages=15)


#%%