from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Vacancy(Base):
    __tablename__ = 'vacancies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String)
    stack = Column(String)
    requirements = Column(Text)
    salary = Column(Float)
    description = Column(Text)

class Resume(Base):
    __tablename__ = 'resumes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    experience = Column(Text)
    stack = Column(String)
    education = Column(Text)
    projects = Column(Text)

class CorporatePolicy(Base):
    __tablename__ = 'corporate_policies'

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String)
    policy_document = Column(Text)