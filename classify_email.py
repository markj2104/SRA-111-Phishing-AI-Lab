# classify_email.py
import joblib
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Load the trained classifier and vectorizer
classifier = joblib.load("email_classifier.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def clean_email_text(text):
    # Basic cleaning of the input email
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"[^a-zA-Z0-9 ]", "", text)
    text = text.lower()
    return text

def predict_email(text):
    cleaned_text = clean_email_text(text)
    vectorized_input = vectorizer.transform([cleaned_text])
    prediction = classifier.predict(vectorized_input)[0]
    confidence = np.max(classifier.predict_proba(vectorized_input)) * 100
    return prediction, confidence

def main():
    print("\n📧 AI Email Classifier (Naive Bayes)")
    print("Type/paste an email and press Enter twice to classify it.")
    print("Press Ctrl+C to exit.\n")

    while True:
        try:
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            email_text = "\n".join(lines)
            label, confidence = predict_email(email_text)
            label_str = "Phishing" if label == 1 else "Benign"
            print(f"\nPrediction: {label_str} (Confidence: {confidence:.2f}%)\n")
        except KeyboardInterrupt:
            print("\nExiting classifier.")
            break

if __name__ == "__main__":
    main()
