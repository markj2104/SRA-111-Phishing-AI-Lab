import os
import pandas as pd
from email import policy
from email.parser import BytesParser

# Function to extract email content from .eml files
def extract_email_content(file_path):
    with open(file_path, 'rb') as file:
        msg = BytesParser(policy=policy.default).parse(file)
        # Extract the email body; adjust depending on email format
        if msg.is_multipart():
            for part in msg.iter_parts():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode('utf-8', errors='ignore')
        else:
            return msg.get_payload(decode=True).decode('utf-8', errors='ignore')

# Function to load .eml files into a DataFrame
def load_emails_to_dataframe(emails_dir):
    emails = []
    for file_name in os.listdir(emails_dir):
        if file_name.endswith('.eml'):
            file_path = os.path.join(emails_dir, file_name)
            email_content = extract_email_content(file_path)
            if email_content:
                emails.append(email_content)
    # Create DataFrame with 'text' column
    df = pd.DataFrame(emails, columns=['text'])
    return df

# Main script logic
if __name__ == "__main__":
    emails_dir = './emails'  # Directory containing the .eml files
    df = load_emails_to_dataframe(emails_dir)

    # Preview the data
    print("Preview of data:")
    print(df.head())

    # Ensure 'text' column exists
    if 'text' not in df.columns:
        print("❌ 'text' column not found in the dataset.")
        exit()

    # Remove rows where 'text' is empty
    df = df[df['text'].str.strip() != '']
    print(f"Columns in dataframe: {df.columns}")

    # Optionally, save the cleaned DataFrame to a CSV file
    df.to_csv('cleaned_emails.csv', index=False)
    print("Dataset prepared and saved to 'cleaned_emails.csv'.")
