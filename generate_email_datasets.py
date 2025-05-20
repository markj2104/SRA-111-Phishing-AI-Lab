import pandas as pd
import random

# Load the dataset
df = pd.read_csv('combined_emails.csv')

# Check the first few rows to confirm it's loaded correctly
print("First few rows of the dataset:")
print(df.head())

# Set a random seed for reproducibility
random.seed(42)

# Create a list to store the datasets
datasets = []

# Generate 3 datasets, each with 10 emails
for i in range(3):
    # Sample 10 emails randomly
    sampled_df = df.sample(n=10, random_state=i)
    # Append to the datasets list
    datasets.append(sampled_df)

# Save each dataset as a separate CSV file
for i, dataset in enumerate(datasets, 1):
    filename = f'sampled_emails_version_{i}.csv'
    dataset.to_csv(filename, index=False)
    print(f'Saved {filename}')

# Optionally, preview the first dataset to ensure it's correct
print("\nPreview of the first dataset:")
print(datasets[0].head())
