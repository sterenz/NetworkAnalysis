#######################
#                     #
# Analysis modules.   #
#                     # 
#######################

# pandas.
import pandas as pd

# networkx.
import networkx as nx

# common utilities.
from common_utils import csv_to_df, convert_to_int

# matplotlib.
import matplotlib.pyplot as plt

# Progress lib.
from progress.bar import ChargingBar
# from progress.spinner import Spinner

# 1. Load Data with Pandas
# Start by loading your CSV files using pandas. The main CSV with token transactions,
# as well as the ones with alphacore labels and exchange labels.

# Defining data types in the csv.
token_transfer_dtype = {
    'token_address'    : 'string',
    'from_address'     : 'string',
    'to_address'       : 'string',
    'value'            : 'string',
    'transaction_hash' : 'string',
    'log_index'        : 'int',
    'block_number'     : 'int'
}

transactions_df = csv_to_df('./datasets/ethereum-exchanges/token_transfers_full.csv', token_transfer_dtype)

# Apply the custom conversion function to the 'value' column
transactions_df['value'] = transactions_df['value'].apply(convert_to_int)

# Convert "object" datatype to "float64"
transactions_df['value'] = pd.to_numeric(transactions_df['value'], errors='coerce')

# Print the data types
print(transactions_df.dtypes)

# Print the values in the 'value' column
print(transactions_df['value'])

# 2. Create the Network

# Create an empty directed graph
G = nx.DiGraph()

# Init a progress bar for the process of Organization resource.
graph_bar = ChargingBar(
        '-- INFO: Creating the graph', 
        max    = len(transactions_df), 
        suffix = '%(percent).1f%% / rem: %(remaining)d / t: %(elapsed)ds'
    )

# Iterate through your dataset
for index, row in transactions_df.iterrows():
    sender = row['from_address']
    receiver = row['to_address']
    value = row['value']
    transaction_hash = row['transaction_hash']
    
    # Add sender and receiver nodes if they don't exist
    if sender not in G:
        G.add_node(sender)
    if receiver not in G:
        G.add_node(receiver)
    
    # Add edge with transaction_hash as a unique identifier and value as an attribute
    G.add_edge(sender, receiver, key=transaction_hash, value=value)
    
    # Increase the progress bar.
    graph_bar.next()

# Stop the progress bar.
graph_bar.finish()

print('-- INFO: Graph has been created.')

# Print basic graph info
print(nx.number_of_nodes(G))
print(nx.number_of_edges(G))

# 3. Visualize the network

# Create a layout for our nodes 
layout = nx.spring_layout(G)

# Draw nodes and edges
nx.draw(G, pos=layout, with_labels=False, node_size=100, font_size=8)

# Show the plot
plt.show()