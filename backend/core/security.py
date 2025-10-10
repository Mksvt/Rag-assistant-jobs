from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    """
    Create a JWT access token.

    Args:
        data (dict): The payload data to encode in the token.

    Returns:
        str: The encoded JWT token.
    """
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password, hashed_password):
    """
    Verify if a plain password matches its hashed version.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Hash a plain text password.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)