import pandas as pd
from minisom import MiniSom
import numpy as np

# Replace 'path_to_your_file' with the actual path to your CSV file
file_path = 'labeled_ddostrace.to-victim.20070804.csv'

# Read the CSV file, skipping the first row
df = pd.read_csv(file_path)

# Convert each column to numeric
df = df.apply(pd.to_numeric, errors='coerce')

# Extract relevant features
features = df[['Frame Length', 'Interpacket Time', 'Port Used', 'Protocol', 'Timestamp']].values

# Normalize features
features = (features - features.min(axis=0)) / (features.max(axis=0) - features.min(axis=0))

# SOM
grid_size = 10
som = MiniSom(grid_size, grid_size, features.shape[1], sigma=0.5, learning_rate=0.5)

# SOM with random weights
som.random_weights_init(features)

num_epochs = 100
som.train_batch(features, num_epochs, verbose=True)

# Reference point G
reference_point = np.median(som._weights.reshape((-1, features.shape[1])), axis=0)

# Calculate distances
distances = np.linalg.norm(features - reference_point, axis=1)

# Set anomaly detection threshold
threshold = 0.95

# Identify anomalies
anomalies = distances > np.percentile(distances, threshold * 100)

print("Anomalies:", anomalies)
