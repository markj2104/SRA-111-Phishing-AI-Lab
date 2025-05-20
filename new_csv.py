import pandas as pd

# Load phishing emails
phishing_df = pd.read_csv('cleaned_emails.csv')  # replace with actual path if different
phishing_sample = phishing_df.sample(n=5, random_state=42)
phishing_sample = phishing_sample.rename(columns={'text': 'message'})
phishing_sample['label'] = 'Phishing'

# Load legitimate emails
legitimate_df = pd.read_csv('cleaned_enron_emails.csv')  # replace with actual path if different
legitimate_sample = legitimate_df.sample(n=5, random_state=42)
legitimate_sample['label'] = 'Legitimate'

# Ensure consistent columns
phishing_sample = phishing_sample[['message', 'label']]
legitimate_sample = legitimate_sample[['message', 'label']]

# Combine
balanced_df = pd.concat([phishing_sample, legitimate_sample])
balanced_df.to_csv('balanced_sampled_emails.csv', index=False)

print("Created balanced_sampled_emails.csv with 5 phishing and 5 legitimate emails.")
