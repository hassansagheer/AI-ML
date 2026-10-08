import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load both datasets
df_original = pd.read_csv('healthcare-dataset-stroke-data.csv')
df_clean = pd.read_csv('healthcare_dataset_stroke.csv')

# Define target variable and key categorical features to compare
features = ['stroke', 'hypertension', 'heart_disease']

fig, axes = plt.subplots(len(features), 2, figsize=(12, 4 * len(features)))

for i, feature in enumerate(features):
    # Plot Original Data Distribution
    sns.countplot(
        data=df_original, 
        x=feature, 
        ax=axes[i, 0], 
        palette='Blues_d'
    )
    axes[i, 0].set_title(f'Original Data: {feature} Distribution (with N/A BMI)')
    axes[i, 0].set_xlabel(feature)
    axes[i, 0].set_ylabel('Count')

    # Plot Cleaned Data Distribution
    sns.countplot(
        data=df_clean, 
        x=feature, 
        ax=axes[i, 1], 
        palette='Greens_d'
    )
    axes[i, 1].set_title(f'Cleaned Data: {feature} Distribution (No N/A BMI)')
    axes[i, 1].set_xlabel(feature)
    axes[i, 1].set_ylabel('Count')

plt.tight_layout()
plt.show()

# Print exact class proportion percentages for comparison
print("--- Original Target Class Ratio (%) ---")
print(df_original['stroke'].value_counts(normalize=True) * 100)

print("\n--- Cleaned Target Class Ratio (%) ---")
print(df_clean['stroke'].value_counts(normalize=True) * 100)