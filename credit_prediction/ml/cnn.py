import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
import numpy
import pandas as pd

seed = 10
numpy.random.seed(seed)
from pandas import read_csv
dataset = pd.read_csv(r'C:\Users\Pavan Reddy\Documents\fyp\credit_prediction\ml\odataset.csv')
dataset.dtypes
df = dataset
df.dtypes

X  = df.iloc[1:30001,1:24].values
Y = df.iloc[1:,25].values
X1  =X[17]

model = Sequential()
model.add(Dense(12, input_dim=23, init='uniform', activation='relu'))
model.add(Dense(8, init='uniform', activation='relu'))
model.add(Dense(1, init='uniform', activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X, Y, epochs=50, batch_size=100)

scores = model.evaluate(X, Y)
X
q = model.predict( np.array( [X1,] )  )
print(q[0])

print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
print("%s: %.2f%%" % (model.metrics_names[0], scores[0]*100))
model.save('cnn.h5')
