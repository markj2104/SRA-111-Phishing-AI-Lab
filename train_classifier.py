import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
from sklearn.utils import resample

# Load datasets
phishing_df = pd.read_csv('cleaned_emails.csv')
enron_df = pd.read_csv('cleaned_enron_emails.csv')

print("Phishing Dataset Columns:", phishing_df.columns)
print("Enron Dataset Columns:", enron_df.columns)

# Rename for consistency
phishing_df.rename(columns={'text': 'message'}, inplace=True)

# Add labels
phishing_df['label'] = 1  # phishing
enron_df['label'] = 0     # legitimate

# Combine
df = pd.concat([phishing_df[['message', 'label']], enron_df[['message', 'label']]])

# Balance the dataset
phishing = df[df['label'] == 1]
legit = df[df['label'] == 0]

legit_downsampled = legit.sample(len(phishing), random_state=42)
balanced_df = pd.concat([phishing, legit_downsampled])

print(f"Balanced Dataset: {balanced_df['label'].value_counts()}")

# Split
X = balanced_df['message']
y = balanced_df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Vectorize
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train
classifier = MultinomialNB()
classifier.fit(X_train_tfidf, y_train)

# Predict
y_pred = classifier.predict(X_test_tfidf)

# Evaluate
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Save model and vectorizer
joblib.dump(classifier, "phishing_model.joblib")
joblib.dump(vectorizer, "vectorizer.joblib")
