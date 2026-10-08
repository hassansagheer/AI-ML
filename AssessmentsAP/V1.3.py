# Import Libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Display settings
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 120
RND = 2026  # random seed

# Load Data function
def Load_Data(path='healthcare-dataset-stroke-data.csv'):
    return pd.read_csv(path)

# Load the dataset
data = Load_Data('healthcare-dataset-stroke-data.csv')

# Remove rows where 'bmi' is missing and save to new file
data_clean = data.dropna(subset=['bmi'])
data_clean.to_csv('healthcare_dataset_stroke.csv', index=False)

# Reload the newly saved dataset
data = pd.read_csv('healthcare_dataset_stroke.csv')

# Check missing values & dataset overview
def overview(df):
    print("Rows / Columns:", df.shape)
    print("\nColumn types:\n", df.dtypes)
    print("\nMissing values per column:\n", df.isna().sum())
    print("\nDescriptive summary (numeric columns):\n", df.describe().T)

overview(data)

print("\nDuplicate rows count:", data.duplicated().sum())

# Display the first few rows (Jupyter will format this cleanly)
data.head()