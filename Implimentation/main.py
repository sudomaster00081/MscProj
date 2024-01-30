import pandas as pd
from minisom import MiniSom
import numpy as np

# Load the dataset

#url = "ddostrace.to-victim.20070804.csv"
url = "ddostrace.to-victim.20070804_134936.csv"

df = pd.read_csv(url)

features = df[['frame.len', 'frame.time_delta_displayed', 'tcp.dstport', 'udp.dstport', 'ip.proto', 'frame.time_relative']].values

# Normalize
features = (features - features.min(axis=0)) / (features.max(axis=0) - features.min(axis=0))

# SOM
grid_size = 10 
som = MiniSom(grid_size, grid_size, features.shape[1], sigma=0.5, learning_rate=0.5)

# SOM with random weights
som.random_weights_init(features)

num_epochs = 100  
som.train_batch(features, num_epochs, verbose=True)

# reference point G
reference_point = np.median(som._weights.reshape((-1, features.shape[1])), axis=0)

#dist
distances = np.linalg.norm(features - reference_point, axis=1)

threshold = 0.95

anomalies = distances > np.percentile(distances, threshold * 100)

print("Anomalies:", anomalies)
