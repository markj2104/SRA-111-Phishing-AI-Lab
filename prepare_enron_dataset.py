import pandas as pd
import os

# Load the dataset
df = pd.read_csv('enron_dataset/emails.csv')

# Show a preview of the data
print("Preview of data:")
print(df.head())

# Check the columns
print("\nColumns in the dataset:")
print(df.columns)

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# Preprocess the 'message' column
df = df.dropna(subset=['message'])  # Remove rows with missing message values

# Clean the 'message' column (strip leading/trailing whitespaces, etc.)
df['message'] = df['message'].str.strip()

# Preview the cleaned data
print("\nCleaned data preview:")
print(df.head())

# Save the cleaned dataset
df.to_csv('cleaned_enron_emails.csv', index=False)

print("\nDataset prepared and saved to 'cleaned_enron_emails.csv'.")
