'''
python test_keras.py [csv] [epochs] [layer sizes]
'''

from sys import argv
import numpy as np
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras import regularizers
from sklearn.metrics import r2_score
import os

layers = argv[3].split(',')
for i in range(0,len(layers)):
	layers[i] = int(layers[i])

os.environ["CUDA_VISIBLE_DEVICES"]="1"

mat = np.loadtxt(open(argv[1], "rb"), delimiter=",", skiprows=1)

np.random.shuffle(mat)

splSz = len(mat) / 5

# train_X = mat[0:3*splSz]
# train_y = train_X[:,1]
# valid_X = mat[3*splSz:4*splSz]
# valid_y = valid_X[:,1]
# test_X = mat[4*splSz:]
# test_y = test_X[:,1]

# train_X = np.delete(train_X, 1, 1)
# valid_X = np.delete(valid_X, 1, 1)
# test_X = np.delete(test_X, 1, 1)

train_X = mat[0:4*splSz]
train_y = train_X[:,1]
test_X = mat[4*splSz:]
test_y = test_X[:,1]

train_X = np.delete(train_X, 1, 1)
test_X = np.delete(test_X, 1, 1)

def train_rep(arr):
	model = Sequential()
	count = 0
	for i in arr:
		if count == 0:
			model.add(Dense(
				i, 
				activation = 'linear', 
				input_shape=(train_X.shape[1],))
			)
		else:
			model.add(Dense(i, activation = 'linear'))
	
	model.add(Dense(1, activation = 'linear'))

	model.summary()

	callbacks = [
		keras.callbacks.EarlyStopping(monitor='loss', min_delta=0, patience=23, verbose=0, mode='auto'),
		keras.callbacks.ReduceLROnPlateau(monitor='loss', factor=0.1, patience=10, verbose=0, mode='auto', epsilon=0.0001, cooldown=0, min_lr=10**-30)
	]

	# optimizer = keras.optimizers.SGD(lr = 10**-5, momentum = 10**1)
	# optimizer = keras.optimizers.RMSprop()
	optimizer = keras.optimizers.Nadam()

	model.compile(loss='mean_absolute_error', optimizer = optimizer)

	history = model.fit(train_X, train_y, batch_size=128, epochs = int(argv[2]), verbose = 1, validation_data=(test_X, test_y), callbacks = callbacks)

	# score = model.evaluate(test_X, test_y, verbose = 0)
	# print score
	# print 'Test loss:    ', str(score[0])
	# print 'Test accuracy:', str(score[1])

	test_P = model.predict(test_X)
	train_P = model.predict(train_X)
	# valid_P = model.predict(valid_X)
	return r2_score(test_y, test_P), r2_score(train_y, train_P)#, r2_score(valid_y, valid_P)

trArr = []
teArr = []
for i in range(0,10):
	trScore, teScore = train_rep(layers)
	trArr.append(trScore)
	teArr.append(teScore)

print np.average(teArr), np.average(trArr), layers


