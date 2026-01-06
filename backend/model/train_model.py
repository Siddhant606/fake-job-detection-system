import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from backend.utils.preprocess import clean_text

df = pd.read_csv('backend/dataset/fake_job_postings.csv')
print(df.head())

df['text'] = (
    df['title'].fillna('') + ' ' +
    df['description'].fillna('')
)
df['text'] = df['text'].apply(clean_text)

X = df['text']
y = df['fraudulent']
vectorizer = TfidfVectorizer(max_features=5000)
X_vec = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

joblib.dump(model, 'backend/model/fake_job_model.pkl')
joblib.dump(vectorizer, 'backend/model/vectorizer.pkl')

