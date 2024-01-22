import pandas as pd
from minisom import MiniSom
import numpy as np

# Load the dataset
url = "ddostrace.to-victim.20070804.csv"
df = pd.read_csv(url)

# Extract relevant features
features = df[['frame.len', 'frame.time_delta_displayed', 'tcp.dstport', 'udp.dstport', 'ip.proto', 'frame.time_relative']].values

# Normalize the features
features = (features - features.min(axis=0)) / (features.max(axis=0) - features.min(axis=0))

# Define SOM parameters
grid_size = 10  # Adjust based on the dataset and desired SOM size
som = MiniSom(grid_size, grid_size, features.shape[1], sigma=0.5, learning_rate=0.5)

# Initialize the SOM with random weights
som.random_weights_init(features)

# Train the SOM with only normal traffic samples
num_epochs = 100  # Adjust based on the dataset and training needs
som.train_batch(features, num_epochs, verbose=True)

# Choose a reference point G (e.g., median values of SOM neurons)
reference_point = np.median(som.weights.reshape((-1, features.shape[1])), axis=0)

# Calculate distances between input samples and the reference point
distances = np.linalg.norm(features - reference_point, axis=1)

# Set a probability threshold (adjust as needed)
threshold = 0.95

# Classify anomalies based on distance to the reference point
anomalies = distances > np.percentile(distances, threshold * 100)

# Print the results or take further actions as needed
print("Anomalies:", anomalies)
