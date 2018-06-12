import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Activation
from keras.optimizers import RMSprop
import keras

import string

# TODO: fill out the function below that transforms the input series 
# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):
    # containers for input/output pairs
    X = []
    y = []

    y = series[window_size:]
    for i in range(len(series) - window_size):
        X.append(series[i:i+window_size])

    # reshape each 
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y),1)

    return X,y


# TODO: build an RNN to perform regression on our time series input/output data
def build_part1_RNN(window_size):
    model = Sequential()
    lstm = LSTM(5, activation='tanh', input_shape=(window_size, 1))
    dense = Dense(1)
    model.add(lstm)
    model.add(dense)
    return model


### TODO: return the text input with only ascii lowercase and the punctuation given below included.
def cleaned_text(text):
    text = text.replace('ã','a')
    punctuation = ['!', ',', '.', ':', ';', '?']
    chars = set(text)
    # in this SO thread we can see some ideas
    # https://stackoverflow.com/questions/16060899/alphabet-range-python/37716814
    for char in chars:
        if char not in string.ascii_lowercase and char not in punctuation and char != ' ':
            text = text.replace(char, '')
    return text

### TODO: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    inputs = []
    outputs = []
    for i in range(0,len(text) - window_size, step_size):
        inputs.append(text[i:i+window_size])
        outputs.append(text[i+window_size])

    return inputs,outputs

# TODO build the required RNN model: 
# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss 
def build_part2_RNN(window_size, num_chars):
    model = Sequential()
    lstm = LSTM(200, input_shape=((window_size,num_chars)))
    dense = Dense(num_chars, activation='softmax')
    #activ = Activation('softmax')
    model.add(lstm)
    model.add(dense)
    #model.add(activ)
    return model
