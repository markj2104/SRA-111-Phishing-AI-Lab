import pandas as pd
import os

# Load the balanced dataset
df = pd.read_csv("balanced_sampled_emails.csv")

# Create a folder to hold the email text files
output_folder = "review_emails"
os.makedirs(output_folder, exist_ok=True)

# Export each email to a separate file
for i, row in df.iterrows():
    with open(f"{output_folder}/email_{i+1}.txt", "w", encoding="utf-8") as f:
        f.write(row["message"])

print(f"{len(df)} emails exported to the '{output_folder}' folder.")
