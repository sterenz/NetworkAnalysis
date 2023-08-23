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

# decimal for big numbers.
from sympy import Integer

# numpy.
import numpy as np

# 1. Load Data with Pandas
# Start by loading your CSV files using pandas. The main CSV with token transactions,
# as well as the ones with alphacore labels and exchange labels.

dtype = {
    'token_address'    : 'string',
    'from_address'     : 'string',
    'to_address'       : 'string',
    'value'            : 'string',
    'transaction_hash' : 'string',
    'log_index'        : 'int',
    'block_number'     : 'int'
}

transactions_df = csv_to_df('./datasets/ethereum-exchanges/token_transfers_test.csv', dtype)

# Apply the custom conversion function to the 'value' column
transactions_df['value'] = transactions_df['value'].apply(convert_to_int)

# Convert "object" datatype to "float64"
transactions_df['value'] = pd.to_numeric(transactions_df['value'], errors='coerce')

# Print the data types
print(transactions_df.dtypes)

# Print the values in the 'value' column
print(transactions_df['value'])