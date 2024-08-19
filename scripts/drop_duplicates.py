import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Drop duplicates from csv file.')
parser.add_argument('input_file', type=str, help='Path to the CSV input file.')

args = parser.parse_args()

df = pd.read_csv(args.input_file)

count_before = df.shape[0]

df = df.drop_duplicates()

count_after = df.shape[0]

print(f'Removed {count_before - count_after} duplicate rows.')

df.to_csv(f'../CIMIS_Flask/data/combined_daily.csv', index=False)
