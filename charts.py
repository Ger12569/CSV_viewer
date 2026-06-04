import matplotlib.pyplot as plt
import os

def create_histogram(df, column, output_path):
    plt.figure()
    df[column].dropna().hist(bins=10)
    plt.title(f"Histogram of {column}")
    plt.savefig(output_path)
    plt.close()