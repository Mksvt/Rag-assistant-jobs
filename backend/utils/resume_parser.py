"""
Resume parser module for extracting skills and information from resumes.

This module provides functions to parse PDF and DOCX files and extract relevant information.
"""

import re
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None  # type: ignore

try:
    from docx import Document
except ImportError:
    Document = None  # type: ignore


def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    if PyPDF2 is None:
        return "PyPDF2 not installed. Install it with: pip install PyPDF2"

    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    except (IOError, OSError) as e:
        return f"Error reading PDF: {str(e)}"
    return text


def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    if Document is None:
        return "python-docx not installed. Install it with: pip install python-docx"

    try:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except (IOError, OSError) as e:
        return f"Error reading DOCX: {str(e)}"
    return text


def extract_text_from_resume(file_path):
    """Extract text from resume file (PDF or DOCX)."""
    file_extension = Path(file_path).suffix.lower()

    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension in ['.docx', '.doc']:
        return extract_text_from_docx(file_path)
    else:
        return "Unsupported file format"


def extract_skills(text):
    """
    Extract skills from resume text using keyword matching.

    This is a basic implementation. In production, you'd use NLP/NER models.
    """
    # Common tech skills keywords - comprehensive list
    common_skills = [
        # Programming Languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c',
        'ruby', 'php', 'go', 'golang', 'rust', 'swift', 'kotlin', 'scala',
        'r', 'matlab', 'perl', 'shell', 'bash', 'powershell', 'vba',
        'objective-c', 'dart', 'elixir', 'haskell', 'lua', 'groovy',
        
        # Web Frontend
        'react', 'angular', 'vue', 'vue.js', 'svelte', 'next.js', 'nuxt.js',
        'html', 'html5', 'css', 'css3', 'sass', 'scss', 'less', 'tailwind',
        'bootstrap', 'material-ui', 'chakra ui', 'jquery', 'webpack',
        'vite', 'babel', 'responsive design', 'ui/ux', 'figma', 'sketch',
        
        # Backend & Frameworks
        'node.js', 'express', 'django', 'flask', 'fastapi', 'spring',
        'spring boot', '.net', 'asp.net', 'laravel', 'symfony', 'rails',
        'ruby on rails', 'gin', 'echo', 'nest.js', 'koa', 'strapi',
        
        # Databases
        'sql', 'nosql', 'postgresql', 'mysql', 'mongodb', 'redis',
        'cassandra', 'elasticsearch', 'oracle', 'sql server', 'mariadb',
        'dynamodb', 'firebase', 'couchdb', 'neo4j', 'influxdb', 'sqlite',
        
        # DevOps & Cloud
        'docker', 'kubernetes', 'k8s', 'aws', 'azure', 'gcp',
        'google cloud', 'heroku', 'digital ocean', 'terraform', 'ansible',
        'jenkins', 'gitlab ci', 'github actions', 'circleci', 'travis ci',
        'ci/cd', 'devops', 'linux', 'unix', 'nginx', 'apache',
        
        # Data Science & ML
        'machine learning', 'deep learning', 'tensorflow', 'pytorch',
        'keras', 'scikit-learn', 'pandas', 'numpy', 'scipy', 'matplotlib',
        'seaborn', 'plotly', 'data analysis', 'data science', 'statistics',
        'nlp', 'computer vision', 'opencv', 'spacy', 'nltk', 'transformers',
        'bert', 'gpt', 'neural networks', 'cnn', 'rnn', 'lstm',
        
        # Mobile Development
        'android', 'ios', 'react native', 'flutter', 'xamarin',
        'ionic', 'cordova', 'swift ui', 'jetpack compose',
        
        # Version Control & Tools
        'git', 'github', 'gitlab', 'bitbucket', 'svn', 'mercurial',
        
        # Testing
        'unit testing', 'integration testing', 'pytest', 'jest', 'mocha',
        'selenium', 'cypress', 'junit', 'testng', 'jasmine', 'karma',
        
        # APIs & Architecture
        'rest api', 'restful', 'graphql', 'soap', 'grpc', 'websocket',
        'microservices', 'monolith', 'event-driven', 'serverless',
        'lambda', 'api gateway', 'message queue', 'rabbitmq', 'kafka',
        
        # Methodologies & Practices
        'agile', 'scrum', 'kanban', 'waterfall', 'tdd', 'bdd', 'ci/cd',
        'pair programming', 'code review', 'design patterns', 'solid',
        
        # Project Management & Collaboration
        'jira', 'confluence', 'trello', 'asana', 'slack', 'teams',
        'notion', 'monday.com',
        
        # Security
        'oauth', 'jwt', 'ssl', 'tls', 'encryption', 'security',
        'penetration testing', 'owasp',
        
        # Other Technologies
        'blockchain', 'ethereum', 'solidity', 'web3', 'smart contracts',
        'iot', 'edge computing', 'big data', 'hadoop', 'spark',
        'etl', 'data warehouse', 'power bi', 'tableau', 'looker',
        
        # Soft Skills (often mentioned in resumes)
        'communication', 'leadership', 'teamwork', 'problem solving',
        'critical thinking', 'time management', 'adaptability',
        
        # HR & Recruitment Skills
        'recruitment', 'talent acquisition', 'sourcing', 'interviewing',
        'onboarding', 'hr management', 'applicant tracking', 'ats',
        'linkedin recruiter', 'boolean search', 'candidate screening',
        'employer branding', 'crm', 'zoho', 'hubspot', 'greenhouse',
        'workday', 'bamboohr', 'performance management',
        
        # Business & Management
        'project management', 'product management', 'business analysis',
        'stakeholder management', 'budget management', 'strategic planning',
        'kpi', 'roi', 'excel', 'powerpoint', 'word', 'google sheets',
        'salesforce', 'erp', 'sap', 'crm systems'
    ]

    text_lower = text.lower()
    found_skills = []

    for skill in common_skills:
        if skill in text_lower:
            found_skills.append(skill)

    return list(set(found_skills))  # Remove duplicates


def extract_experience_years(text):
    """
    Extract years of experience from resume text.

    Looks for patterns like "X years", "X+ years", etc.
    """
    patterns = [
        r'(\d+)\+?\s*(?:years?|yrs?)',
        r'experience[:\s]+(\d+)\+?\s*(?:years?|yrs?)',
    ]

    text_lower = text.lower()
    years = []

    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        years.extend([int(match) for match in matches])

    return max(years) if years else 0


def analyze_resume(file_path):
    """
    Analyze a resume file and extract key information.

    Returns:
        dict: Dictionary containing extracted information
    """
    text = extract_text_from_resume(file_path)

    if "Error" in text or "not installed" in text:
        return {
            "error": text,
            "skills": [],
            "experience_years": 0,
            "text_preview": ""
        }

    skills = extract_skills(text)
    experience_years = extract_experience_years(text)

    return {
        "skills": skills,
        "experience_years": experience_years,
        "text_preview": text[:500] if text else "",
        "total_skills_found": len(skills)
    }
