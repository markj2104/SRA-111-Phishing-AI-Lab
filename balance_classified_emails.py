import pandas as pd

# Load the classified emails dataset
df = pd.read_csv('classified_sampled_emails.csv')

# Split the dataset into phishing and legitimate emails
phishing_emails = df[df['label'] == 'Phishing']
legitimate_emails = df[df['label'] == 'Legitimate']

# Check the number of phishing and legitimate emails
print("Number of phishing emails:", phishing_emails.shape[0])
print("Number of legitimate emails:", legitimate_emails.shape[0])

# Sample 5 phishing and 5 legitimate emails if there are enough emails in the dataset
if phishing_emails.shape[0] >= 5 and legitimate_emails.shape[0] >= 5:
    phishing_sample = phishing_emails.sample(n=5, random_state=42)
    legitimate_sample = legitimate_emails.sample(n=5, random_state=42)

    # Combine the samples into one balanced dataset
    balanced_df = pd.concat([phishing_sample, legitimate_sample])

    # Save the balanced dataset to a new CSV file
    balanced_df.to_csv('balanced_sampled_emails.csv', index=False)
    print("Balanced dataset created with 5 phishing and 5 legitimate emails.")
else:
    print("Not enough emails to sample from.")
