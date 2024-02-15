import numpy as np
import pandas as pd
from minisom import MiniSom
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score

# Load the dataset
data = pd.read_csv("labeled_ddostrace.to-victim.20070804.csv")

# Convert other columns to appropriate data types
data['Source IP'] = data['Source IP'].astype(str)
data['Destination IP'] = data['Destination IP'].astype(str)
data['Protocol'] = pd.to_numeric(data['Protocol'], errors='coerce') # if it's numeric
data['Frame Length'] = pd.to_numeric(data['Frame Length'], errors='coerce') # if it's numeric
data['Port Used'] = pd.to_numeric(data['Port Used'], errors='coerce') # if it's numeric
data['Interpacket Time'] = pd.to_numeric(data['Interpacket Time'], errors='coerce') # if it's numeric
data['Entropy'] = pd.to_numeric(data['Entropy'], errors='coerce') # if it's numeric
data['label'] = pd.to_numeric(data['label'], errors='coerce') # if it's numeric

# Drop rows with missing values
data.dropna(inplace=True)

# Separate features and labels
X = data.drop(['label', 'Timestamp', 'Source IP', 'Destination IP'], axis=1).values
y = data['label'].values

# Normalize features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Define SOM parameters
som_grid_rows = 10
som_grid_columns = 10
input_len = X_scaled.shape[1]

# Train SOM
som = MiniSom(som_grid_rows, som_grid_columns, input_len, sigma=1.0, learning_rate=0.5)
som.random_weights_init(X_scaled)

# Define number of iterations and print frequency
num_iterations = 10000
print_frequency = 1000

# Training SOM with progress indicator
for i in range(num_iterations):
    percent_complete = (i + 1) / num_iterations * 100
    if (i + 1) % print_frequency == 0:
        print(f"Training SOM: {percent_complete:.2f}% complete")
    som.train_random(X_scaled, 1)

print("Training SOM: 100.00% complete")

# Find the winning neurons for each sample
winning_neurons = np.array([som.winner(x) for x in X_scaled])

# Assign labels to clusters based on the majority label of the samples in each cluster
cluster_labels = []
total_samples = len(winning_neurons)

for i, neuron in enumerate(winning_neurons):
    cluster_samples_indices = np.where((winning_neurons[:, 0] == neuron[0]) & (winning_neurons[:, 1] == neuron[1]))[0]
    cluster_labels.append(y[cluster_samples_indices].mean())

    # Print progress
    if (i + 1) % print_frequency == 0 or i + 1 == total_samples:
        percent_complete = (i + 1) / total_samples * 100
        print(f"Assigning cluster labels: {percent_complete:.2f}% complete")

# Evaluate accuracy
accuracy = accuracy_score(y, cluster_labels)
print("Accuracy:", accuracy)
