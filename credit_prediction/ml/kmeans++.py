import sys
import numpy as np
from numpy import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.ndimage.interpolation import shift
dataset = pd.read_csv(r'C:\Users\Pavan Reddy\Documents\fyp\credit_prediction\ml\dataset.csv')
X  = df.iloc[1:30001,1:24].values
from sklearn.cluster import KMeans
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)
plt.plot(range(1, 11), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()
kmeans = KMeans(n_clusters=2, init='k-means++', max_iter=300, n_init=10, random_state=0)
y_kmeans = kmeans.fit_predict(X)
y_kmeans1 = array(range(30001),dtype='str').reshape(30001)
y_kmeans1.shape
y_kmeans1[0]="kmeans"
for i in range(30000):
        y_kmeans1[i+1]=y_kmeans[i]
        i=i+1
dataset['Y0']=y_kmeans1
dataset.to_csv(r'C:\Users\Pavan Reddy\Desktop\kmeans\odataset.csv', index=False)