import pandas as pd
from minisom import MiniSom
from sklearn.preprocessing import MinMaxScaler

# Load the dataset
data = pd.read_csv("labeled_ddostrace.to-victim.20070804.csv")
# Print the column types
print(data.dtypes)

# Convert 'Timestamp' column to datetime
# data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s')

# Convert other columns to appropriate data types
data['Source IP'] = data['Source IP'].astype(str)
data['Destination IP'] = data['Destination IP'].astype(str)
data['Protocol'] = pd.to_numeric(data['Protocol'], errors='coerce') # if it's numeric
data['Frame Length'] = pd.to_numeric(data['Frame Length'], errors='coerce') # if it's numeric
data['Port Used'] = pd.to_numeric(data['Port Used'], errors='coerce') # if it's numeric
data['Interpacket Time'] = pd.to_numeric(data['Interpacket Time'], errors='coerce') # if it's numeric
data['Entropy'] = pd.to_numeric(data['Entropy'], errors='coerce') # if it's numeric
data['label'] = pd.to_numeric(data['label'], errors='coerce') # if it's numeric

# Now, the DataFrame should have appropriate data types

# Print the column types
print(data.dtypes)

# Display the first few rows of the dataset
print(data.head())
from sklearn.preprocessing import MinMaxScaler

# Drop Timestamp column
data = data.drop(columns=['Timestamp'])

# Normalize numerical features
scaler = MinMaxScaler()
data[['Frame Length', 'Port Used', 'Interpacket Time', 'Entropy']] = scaler.fit_transform(data[['Frame Length', 'Port Used', 'Interpacket Time', 'Entropy']])
data = data[['Frame Length', 'Port Used', 'Interpacket Time', 'Entropy']]
# Display the updated dataset
print(data.head())


from minisom import MiniSom

# Define SOM parameters (you may need to adjust these based on your data)
grid_size = (10, 10)  # Size of the SOM grid
input_len = len(data.columns)  # Number of input features
sigma = 1.0  # Spread of the neighborhood function
learning_rate = 0.5  # Initial learning rate

# Initialize the SOM
som = MiniSom(grid_size[0], grid_size[1], input_len, sigma=sigma, learning_rate=learning_rate)

print(data.head())
# Initialize weights
som.random_weights_init(data.values)

# Train the SOM
num_iterations = 1000  # Number of iterations
som.train_random(data.values, num_iterations)

# Map each data point to its closest neuron
mapped = som.win_map(data.values)

# Calculate the number of data points in each neuron
cluster_sizes = [len(mapped[(i, j)]) for i in range(grid_size[0]) for j in range(grid_size[1])]
print("Cluster sizes:", cluster_sizes)
import matplotlib.pyplot as plt
import numpy as np

# Create a meshgrid for the SOM
xx, yy = np.meshgrid(np.arange(0, grid_size[0]), np.arange(0, grid_size[1]))

# Plot the SOM clusters
plt.figure(figsize=(10, 8))
plt.pcolor(xx, yy, np.array(cluster_sizes).reshape(grid_size[0], grid_size[1]), cmap='Blues')  # You can use any colormap you prefer
plt.colorbar(label='Number of data points')
plt.title('Self-Organizing Map Clusters')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()


