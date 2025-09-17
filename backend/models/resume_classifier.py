from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import joblib

class ResumeClassifier:
    def __init__(self):
        self.model = make_pipeline(TfidfVectorizer(), LogisticRegression())
    
    def train(self, X, y):
        self.model.fit(X, y)
    
    def predict(self, resumes):
        return self.model.predict(resumes)
    
    def save_model(self, file_path):
        joblib.dump(self.model, file_path)
    
    def load_model(self, file_path):
        self.model = joblib.load(file_path)