import pandas as pd
import joblib

# Load the trained model and vectorizer
model = joblib.load('phishing_model.joblib')
vectorizer = joblib.load('vectorizer.joblib')

# Load sample emails
df = pd.read_csv('balanced_sampled_emails.csv')  # adjust filename if needed

# Make sure the column is named 'message'
if 'message' not in df.columns:
    # Try renaming from 'text' or 'content' or similar
    for col in df.columns:
        if 'text' in col.lower() or 'content' in col.lower():
            df.rename(columns={col: 'message'}, inplace=True)
            break

# Drop missing values
df.dropna(subset=['message'], inplace=True)

# Transform the messages into TF-IDF features
X_tfidf = vectorizer.transform(df['message'])

# Predict using the model
predictions = model.predict(X_tfidf)

# Attach predictions to dataframe
df['prediction'] = predictions
df['label'] = df['prediction'].map({0: 'Legitimate', 1: 'Phishing'})

# Print results
print(df[['message', 'label']].head(10))  # Show first 10 for quick check

# Optional: Save results to CSV
df.to_csv('classified_sampled_emails.csv', index=False)
print("Classification complete. Results saved to classified_sampled_emails.csv.")
