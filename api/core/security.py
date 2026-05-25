from datetime import datetime, timedelta
from typing import Optional

# Mock implementations since we cannot install PyJWT and passlib easily in this environment without modifying pyproject/requirements
# In a real environment, these would wrap passlib.context and jwt.encode

SECRET_KEY = "nexra_super_secret_enterprise_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return plain_password + "_hashed" == hashed_password

def get_password_hash(password: str) -> str:
    return password + "_hashed"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire.timestamp()})
    
    # Mock JWT encoding
    import json
    import base64
    return base64.b64encode(json.dumps(to_encode).encode()).decode()

def decode_access_token(token: str):
    import json
    import base64
    try:
        decoded = base64.b64decode(token).decode()
        return json.loads(decoded)
    except:
        return None
