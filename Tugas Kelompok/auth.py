from datetime import datetime, timedelta
import os
import jwt
from dotenv import load_dotenv
from typing import Dict, Any


load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET", "dev_secret_not_for_prod")
ALGORITHM = "HS256"


def create_access_token(subject: str, email: str, expires_minutes: int = 15) -> str:
    now = datetime.utcnow()
    payload: Dict[str, Any] = {
    "sub": subject,
    "email": email,
    "iat": now,
    "exp": now + timedelta(minutes=expires_minutes)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
    return token


def decode_access_token(token: str) -> Dict[str, Any]:
    import jwt
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")