# This script is used to read all .xpt files in a directory and plot basic analytics
# Specific data files are only available in the remote desktop environment

import numpy as np
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns

# Function to read all .xpt files in the data directory
def read_xpt_files(directory):
    xpt_files = glob.glob(os.path.join(directory, '*.xpt'))
    dataframes = {}
    for file in xpt_files:
        df = pd.read_sas(file, format='xport')
        # Generate pseudo ID if any column looks like an ID
        for col in df.columns:
            if 'id' in col.lower():
                df['pseudo_id'] = [f'P{str(i).zfill(4)}' for i in range(len(df))]
                df = df.drop(columns=[col])
        dataframes[os.path.basename(file)] = df
    return dataframes

# Function to summarize DataFrame
def summarize_df(df):
    summary = {
        'num_rows': len(df),
        'num_columns': len(df.columns),
        'columns': list(df.columns),
        'dtypes': df.dtypes.astype(str).to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'head': df.head(3).to_dict(orient='records')
    }
    return summary

# Function to plot basic analytics
def plot_analytics(df, out_prefix):
    # Barplot for first categorical column
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    num_cols = df.select_dtypes(include=[np.number]).columns
    if len(cat_cols) > 0:
        plt.figure(figsize=(8,4))
        sns.countplot(data=df, x=cat_cols[0])
        plt.title(f'Barplot of {cat_cols[0]}')
        plt.tight_layout()
        plt.savefig(f'{out_prefix}_barplot.png')
        plt.close()
    # Boxplot for first numeric column
    if len(num_cols) > 0:
        plt.figure(figsize=(8,4))
        sns.boxplot(data=df, y=num_cols[0])
        plt.title(f'Boxplot of {num_cols[0]}')
        plt.tight_layout()
        plt.savefig(f'{out_prefix}_boxplot.png')
        plt.close()
    # Scatterplot for first two numeric columns
    if len(num_cols) > 1:
        plt.figure(figsize=(8,6))
        sns.scatterplot(data=df, x=num_cols[0], y=num_cols[1])
        plt.title(f'Scatterplot of {num_cols[0]} vs {num_cols[1]}')
        plt.tight_layout()
        plt.savefig(f'{out_prefix}_scatterplot.png')
        plt.close()

if __name__ == '__main__':
    xpt_dir = './'  # Path to data directory
    dataframes = read_xpt_files(xpt_dir)
    for fname, df in dataframes.items():
        print(f'\nSummary for {fname}:')
        summary = summarize_df(df)
        for k, v in summary.items():
            print(f'{k}: {v}')
        out_prefix = fname.replace('.xpt', '')
        plot_analytics(df, out_prefix)
        print(f'Plots saved as {out_prefix}_barplot.png, {out_prefix}_boxplot.png, {out_prefix}_scatterplot.png (if applicable).')
