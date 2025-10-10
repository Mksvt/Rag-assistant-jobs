"""
Script for data ingestion into the database.

This script provides functions to load vacancies, resumes, and corporate policies into the database.
"""

import os
import pandas as pd
from sqlalchemy import create_engine
from backend.database.session import SessionLocal
from backend.database.models import Vacancy, Resume, CorporatePolicy

def load_vacancies(file_path):
    """
    Load vacancies from a CSV file into the database.

    Args:
        file_path (str): Path to the CSV file containing vacancy data.
    """
    vacancies_df = pd.read_csv(file_path)
    engine = create_engine('postgresql://user:password@localhost/dbname')
    vacancies_df.to_sql(Vacancy.__tablename__, engine, if_exists='append', index=False)

def load_resumes(directory_path):
    """
    Load resumes from a directory into the database.

    Args:
        directory_path (str): Path to the directory containing resume files.
    """
    engine = create_engine('postgresql://user:password@localhost/dbname')
    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf') or filename.endswith('.docx'):
            # Logic to extract data from resumes
            resume_data = extract_resume_data(os.path.join(directory_path, filename))
            resume = Resume(**resume_data)
            db = SessionLocal()
            db.add(resume)
            db.commit()
            db.close()

def load_corporate_policies(directory_path):
    """
    Load corporate policies from a directory into the database.

    Args:
        directory_path (str): Path to the directory containing policy files.
    """
    engine = create_engine('postgresql://user:password@localhost/dbname')
    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf') or filename.endswith('.docx'):
            # Logic to extract data from corporate policies
            policy_data = extract_policy_data(os.path.join(directory_path, filename))
            policy = CorporatePolicy(**policy_data)
            db = SessionLocal()
            db.add(policy)
            db.commit()
            db.close()

def main():
    """
    Main function to load all data into the database.
    """
    load_vacancies('data/vacancies/vacancies.csv')
    load_resumes('data/resumes')
    load_corporate_policies('data/policies')

if __name__ == "__main__":
    main()