import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
dataset = pd.read_csv("data.csv", encoding= 'ISO-8859-1')

dataset.head()

print("loading dataset")
dataset = dataset.to_numpy() #A la base c'est un fichier pandas, je passe le fichier en numpy pour l'algo

print("cleaning dataset")
neg_rows = np.any(dataset <= 0, axis=1)

dataset = dataset[~neg_rows]

neg_rows = np.any(dataset >= 1, axis=1)

dataset = dataset[~neg_rows]

lower_bound = 0.35
upper_bound = 0.45

row_indices, col_indices = np.where(np.logical_and(dataset >= lower_bound, dataset <= upper_bound))
indices_to_keep = np.random.choice(len(row_indices), size=int(len(row_indices) * 0.95), replace=False)

row_indices_to_keep = row_indices[indices_to_keep]
col_indices_to_keep = col_indices[indices_to_keep]
dataset = np.delete(dataset, np.column_stack((row_indices_to_keep, col_indices_to_keep)), axis=0)


n_clusters = 4
kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=300).fit(dataset)



# Représentation des clusters
plt.figure(figsize=(8, 6))

# Scatter plot with labels
scatter = plt.scatter(dataset[:, 0], dataset[:, 1], c=kmeans.labels_.astype(float))
plt.xlabel('vpip')
plt.ylabel('largeur')
plt.title("VPIP et largeur des bots")

# Create a legend
legend_labels = list(set(kmeans.labels_))  # Get unique labels
plt.legend(handles=scatter.legend_elements()[0], labels=legend_labels, title="Labels")

# Show the plot
plt.show()

with open('model.pkl', 'wb') as file:
    pickle.dump(kmeans, file)