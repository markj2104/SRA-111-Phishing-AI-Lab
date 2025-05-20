import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# 1. Load and prepare your data (Ensure 'message' and 'label' columns are correct)
# Assuming phishing_df and enron_df are loaded correctly with appropriate columns

# Example: Assuming you have 'message' for the email content and 'label' for the classification (0=benign, 1=phishing)
# If the column names differ, adjust as needed
phishing_df = pd.read_csv('path_to_phishing_data.csv')  # Update path if needed
enron_df = pd.read_csv('path_to_enron_data.csv')  # Update path if needed

# Combine datasets
phishing_df['label'] = 1  # Mark phishing emails as 1
enron_df['label'] = 0  # Mark enron emails as 0 (benign)

# Combine both datasets
df = pd.concat([phishing_df[['message', 'label']], enron_df[['message', 'label']]])

# 2. Preprocess and split data
X = df['message']  # Email text
y = df['label']  # Labels (0=benign, 1=phishing)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 3. Create and train the model
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Train the model
model.fit(X_train, y_train)

# 4. Save the model
joblib.dump(model, 'email_classifier.pkl')
print("Model saved as 'email_classifier.pkl'")

# 5. Evaluate the model on test data
y_pred = model.predict(X_test)
print("Classification Report:\n", classification_report(y_test, y_pred))

# 6. Load the model and test it on a new email (for classifying emails)
# You can comment the lines below if not needed immediately
loaded_model = joblib.load('email_classifier.pkl')

# Example usage of the model to classify a new email
new_email = ["Click here to win a prize!"]
prediction = loaded_model.predict(new_email)
print("Prediction for new email:", "Phishing" if prediction[0] == 1 else "Benign")

