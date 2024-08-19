import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

dir = '../'

output_file = './combined_daily.csv'

pattern = os.path.join(dir, 'daily*.csv')

csv_files = glob.glob(pattern)

dataframes = []

for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)

columns_to_drop = [col for col in combined_df.columns if col.startswith('qc')]
print(f'Dropping columns: {columns_to_drop}')

combined_df = combined_df.drop(columns=columns_to_drop)

combined_df = combined_df.dropna()

combined_df['Date'] = pd.to_datetime(combined_df['Date'], errors='coerce')

combined_df = combined_df.sort_values(by=['Date', 'Stn Id'], ascending=[True, True])

combined_df.to_csv(output_file, index=False)

print(combined_df.head())

print(f'CSV files written to {output_file}.')
