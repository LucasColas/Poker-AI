import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle
from sklearn.cluster import KMeans
dataset = pd.read_csv("data.csv", encoding= 'ISO-8859-1')

dataset.head()

print("loading dataset")
dataset = dataset.to_numpy() #A la base c'est un fichier pandas, je passe le fichier en numpy pour l'algo

print("cleaning dataset")
neg_rows = np.any(dataset <= 0, axis=1)

dataset = dataset[~neg_rows]

n_clusters = 4
kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=10).fit(dataset)


with open('model.pkl', 'wb') as file:
    pickle.dump(kmeans, file)