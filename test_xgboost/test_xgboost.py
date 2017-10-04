'''
python test_keras.py [csv] [iterations]
'''

from sys import argv
import numpy as np
# import keras
# from keras.datasets import mnist
# from keras.models import Sequential
# from keras.layers import Dense, Dropout
# from keras import regularizers
from sklearn.metrics import r2_score
import os
import xgboost as xgb

# layers = argv[3].split(',')
# for i in range(0,len(layers)):
# 	layers[i] = int(layers[i])

# os.environ["CUDA_VISIBLE_DEVICES"]="1"

mat = np.loadtxt(open(argv[1], "rb"), delimiter=",", skiprows=1)

np.random.shuffle(mat)

splSz = len(mat) / 5

train_X = mat[0:3*splSz]
train_y = train_X[:,1]
valid_X = mat[3*splSz:4*splSz]
valid_y = valid_X[:,1]
test_X = mat[4*splSz:]
test_y = test_X[:,1]

train_X = np.delete(train_X, 1, 1)
valid_X = np.delete(valid_X, 1, 1)
test_X = np.delete(test_X, 1, 1)

# train_X = mat[0:4*splSz]
# train_y = train_X[:,1]
# test_X = mat[4*splSz:]
# test_y = test_X[:,1]

# train_X = np.delete(train_X, 1, 1)
# test_X = np.delete(test_X, 1, 1)

# trArr = []
# teArr = []
# vaArr = []
# for i in range(0,10):
# 	trScore, teScore = train_rep(layers)
# 	trArr.append(trScore)
# 	teArr.append(teScore)

# print np.average(teArr), np.average(trArr), layers

train = xgb.DMatrix(train_X, label=train_y)
valid = xgb.DMatrix(valid_X, label=valid_y)
test = xgb.DMatrix(test_X, label=test_y)

evals = [(valid, 'eval'), (train, 'train')]

params = {}
params['max_depth'] = 10
params['nthread'] = 14
params['eta'] = 0.0625
params['eval_metric'] = 'mae'

model = xgb.train(params, train, int(argv[2]), evals = evals, early_stopping_rounds = 25)

trPred = model.predict(train)
vaPred = model.predict(valid)
tePred = model.predict(test)

print r2_score(train_y, trPred), r2_score(valid_y, vaPred), r2_score(test_y, tePred), params, argv[2]


