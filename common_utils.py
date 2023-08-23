###########################
#                         #
# Common Utils modules.   #
#                         # 
###########################

# pandas.
from pandas import DataFrame, read_csv

# re.
import re

# decimal.
from decimal import Decimal

# numpy.
import numpy as np

# Function to read CSV into DataFrame
def csv_to_df(_f_path: str, _dtype: dict) -> DataFrame:
    try:
        data_frame = read_csv(
                        _f_path, 
                        keep_default_na = False, 
                        dtype           = _dtype, 
                        sep             = ',',
                        encoding        = 'utf-8'
                    )
        return data_frame
    except Exception:
        print('-- ERR: csv file is empty or malformed!')
        raise
    
# Function to convert to int with high precision
def convert_to_int(value):
    try:
        if 'e' in value or 'E' in value:  # Scientific notation
            # Remove commas
            number_str = value.replace(',', '')
            
            # Extract mantissa and exponent using regular expression
            match = re.match(r'^([0-9.]+)[eE]([+-]?[0-9]+)$', number_str)
            
            if match:
                mantissa = Decimal(match.group(1))
                exponent = int(match.group(2))
                return int(mantissa * (10 ** exponent))
            else:
                return None  # Unable to parse
        else:  # Regular number
            return np.int64(value)
    except:
        return None  # Unable to convert