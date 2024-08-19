import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import argparse

parser = argparse.ArgumentParser(description='Plot data and perform linear regression.')
parser.add_argument('input_file', type=str, help='Path to the CSV input file.')
parser.add_argument('stn_id', type=int, help='Id of CIMIS station')
parser.add_argument('column_to_plot', type=str, help='Data column name to plot.')

args = parser.parse_args()

df = pd.read_csv(args.input_file)

stn_id = args.stn_id
column_to_plot = args.column_to_plot

if column_to_plot not in df.columns:
    raise ValueError(f'Column {column_to_plot} does not exist in the data.')

filtered_df = df[df['Stn Id'] == stn_id].copy()

if filtered_df.empty:
    raise ValueError(f'No data found for station ID {stn_id}')

stn_name = filtered_df['Stn Name'].iloc[0]

filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])

filtered_df['Date_Ordinal'] = filtered_df['Date'].apply(lambda x: x.toordinal())

x = filtered_df[['Date_Ordinal']]
y = filtered_df[column_to_plot]

model = LinearRegression()
model.fit(x,y)

filtered_df['Avg_Air_Temp_Regression'] = model.predict(x)

tick_interval = max(1, len(filtered_df) // 15)

# Plot data with linear regression
print(f'Showing a time lapse of station {stn_id}\'s {column_to_plot}:')

plt.figure(figsize=(12,6))
plt.plot(
        filtered_df['Date'],
        filtered_df[column_to_plot],
        marker='.',
        markersize=0.7,
        linestyle='-',
        linewidth=0.5,
        color='b',
        label='Actual Data'
    )
plt.plot(
        filtered_df['Date'],
        filtered_df['Avg_Air_Temp_Regression'],
        linestyle='--',
        linewidth=3,
        color='r',
        label='Line of best fit'
    )
plt.title(f'{column_to_plot} for station {stn_id}, {stn_name}')
plt.xlabel('Date')
plt.legend()
plt.ylabel(f'{column_to_plot}')
plt.grid(True)
plt.xticks(
        ticks=filtered_df['Date'][::tick_interval],
        labels=filtered_df['Date'][::tick_interval],
        rotation=45
    )
plt.tight_layout()

plt.show()
