"""
Read a frequency table of text features and determine for each
feature wether it is probably sampled from a gaussian normal
distribution.
"""

import pandas as pd
from scipy.stats import normaltest


#Adjust these variables:
CONFIDENCE = 0.001
FILENAME = 'table_with_frequencies.csv'
CSV_SEP = ' '


#Actual script
column_name = f'is_norm_{CONFIDENCE}'
is_norm = lambda row: normaltest(row)[1] < CONFIDENCE
df = pd.read_csv(FILENAME, sep=CSV_SEP, index_col=0)
df[column_name] = df.apply(is_norm, axis=1)

print(f"{len(df[df[column_name]])} of {len(df)} features are considered normally",
      f"distributed with p<{CONFIDENCE}.")
