import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load sample emails (without a header, add column names)
df = pd.read_csv("sampled_emails_version_1.csv", header=None, names=["email_text", "your_label"], quoting=1)

# Load trained model and vectorizer
model = joblib.load("phishing_model.joblib")
vectorizer = joblib.load("vectorizer.joblib")

# Vectorize email text
X_test = vectorizer.transform(df["email_text"])
y_test = df["your_label"]

# Predict
y_pred = model.predict(X_test)

# Output results
print("\n=== Prediction Results ===")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Optional: see mismatches
mismatches = df[y_test != y_pred]
print(f"\nTotal mismatches: {len(mismatches)}")
if not mismatches.empty:
    print("\nExamples of mismatches:")
    print(mismatches.head(3))
