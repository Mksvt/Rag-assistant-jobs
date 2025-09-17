from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import XGBClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib

class MLService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.classifier = LogisticRegression()  # or XGBClassifier()
        self.model_pipeline = Pipeline([
            ('vectorizer', self.vectorizer),
            ('classifier', self.classifier)
        ])

    def train_model(self, resumes, labels):
        X_train, X_test, y_train, y_test = train_test_split(resumes, labels, test_size=0.2, random_state=42)
        self.model_pipeline.fit(X_train, y_train)
        accuracy = self.model_pipeline.score(X_test, y_test)
        return accuracy

    def predict(self, resume):
        return self.model_pipeline.predict([resume])

    def save_model(self, file_path):
        joblib.dump(self.model_pipeline, file_path)

    def load_model(self, file_path):
        self.model_pipeline = joblib.load(file_path)