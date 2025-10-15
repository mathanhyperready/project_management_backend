from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
import hashlib
import bcrypt
from typing import Dict, Any

# -------------------------------
# Load environment variables
# -------------------------------
print("[DEBUG] Loading environment variables...")
load_dotenv()

# -------------------------------
# Password hashing context
# -------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print("[DEBUG] CryptContext initialized with bcrypt")

# -------------------------------
# Environment variables
# -------------------------------
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

print(f"[DEBUG] SECRET_KEY: {'SET' if SECRET_KEY else 'NOT SET'}")
print(f"[DEBUG] ALGORITHM: {ALGORITHM}")
print(f"[DEBUG] ACCESS_TOKEN_EXPIRE_MINUTES: {ACCESS_TOKEN_EXPIRE_MINUTES}")

if not SECRET_KEY:
    raise ValueError("[ERROR] SECRET_KEY is not set in environment variables")

# -------------------------------
# Password utilities
# -------------------------------
def hash_password(password: str) -> str:
    print(f"[DEBUG] Original password: {password}")

    # SHA256 digest as bytes
    sha256_bytes = hashlib.sha256(password.encode("utf-8")).digest()
    print(f"[DEBUG] SHA256 bytes (length {len(sha256_bytes)}): {sha256_bytes.hex()}")

    # Generate bcrypt salt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(sha256_bytes, salt)
    print(f"[DEBUG] bcrypt hashed password: {hashed.decode()}")

    return hashed.decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    sha256_bytes = hashlib.sha256(plain_password.encode("utf-8")).digest()
    print(f"[DEBUG] SHA256 bytes for verification: {sha256_bytes.hex()}")

    result = bcrypt.checkpw(sha256_bytes, hashed_password.encode())
    print(f"[DEBUG] Password verification result: {result}")
    return result

# -------------------------------
# JWT token utilities
# -------------------------------
def create_access_token(data: Dict[str, Any], expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode = data.copy()
    to_encode.update({"exp": expire})

    print(f"[DEBUG] Creating JWT token with payload: {to_encode}")

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"[DEBUG] JWT token: {token}")
    
    return token


def decode_access_token(token: str) -> Dict[str, Any]:
    print(f"[DEBUG] Decoding JWT token: {token}")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"[DEBUG] Decoded payload: {payload}")
        return payload
    except JWTError as e:
        print(f"[ERROR] JWT decoding error: {e}")
        raise ValueError(f"Invalid token: {str(e)}") from e