import pandas as pd

# Load phishing dataset
phishing_df = pd.read_csv("cleaned_emails.csv")  # Your phishing dataset
phishing_df = phishing_df.rename(columns={"text": "message"})
phishing_df["label"] = 1  # Label phishing as 1

# Load Enron dataset (benign emails)
enron_df = pd.read_csv("cleaned_enron_emails.csv")
enron_df["label"] = 0  # Label benign as 0

# Combine and shuffle
combined_df = pd.concat([phishing_df[["message", "label"]], enron_df[["message", "label"]]])
combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save the combined dataset
combined_df.to_csv("combined_emails.csv", index=False)

print("✅ Combined dataset saved to 'combined_emails.csv'")
print("Shape of combined dataset:", combined_df.shape)
print("Preview:")
print(combined_df.head())
