import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
from models.resume_classifier import ResumeClassifier
from models.skill_extractor import SkillExtractor

def load_data(vacancy_file, resume_file):
    vacancies = pd.read_csv(vacancy_file)
    resumes = pd.read_csv(resume_file)
    return vacancies, resumes

def preprocess_data(vacancies, resumes):
    # Implement preprocessing steps such as cleaning and feature extraction
    return processed_vacancies, processed_resumes

def train_model(processed_vacancies, processed_resumes):
    X = processed_resumes.drop('target', axis=1)
    y = processed_resumes['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = ResumeClassifier()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f'Model accuracy: {accuracy:.2f}')

    joblib.dump(model, 'resume_classifier_model.pkl')

if __name__ == "__main__":
    vacancies, resumes = load_data('data/vacancies/vacancies.csv', 'data/resumes/resumes.csv')
    processed_vacancies, processed_resumes = preprocess_data(vacancies, resumes)
    train_model(processed_vacancies, processed_resumes)