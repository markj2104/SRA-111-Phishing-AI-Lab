import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Step 1: Load the CSV file containing emails
emails_df = pd.read_csv("sampled_emails_version_1.csv")

# Step 2: Inspect the first few rows of the dataframe to understand the structure
print(emails_df.head())
print(emails_df.columns)  # Added to check column names

# Step 3: Prepare the data
X = emails_df['message']  # Corrected to the actual column name in your file
y = emails_df['label']     # Assuming the column for labels is 'label'

# Step 4: Preprocess the text data (vectorization)
vectorizer = TfidfVectorizer(stop_words='english')
X_vect = vectorizer.fit_transform(X)

# Step 5: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_vect, y, test_size=0.3, random_state=42)

# Step 6: Train a Logistic Regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Step 7: Evaluate the model on the test set
y_pred = model.predict(X_test)
print("Classification Report for the model:")
print(classification_report(y_test, y_pred))

# Step 8: Save the trained model and vectorizer (optional but recommended)
joblib.dump(model, 'phishing_classifier.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

# Step 9: Test the model with a new email (example)
new_email = ["Congratulations! You have won a free iPhone! Click here to claim your prize."]
new_email_vect = vectorizer.transform(new_email)  # Vectorize the new email
prediction = model.predict(new_email_vect)
print("Prediction for the new email (1 = phishing, 0 = legitimate):", prediction)
