from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt


SECRET_KEY = "b521d3d1b56fe661b177afb0a1fbb7f1b054aa7473956739d5a2a8f93b8d9bcf"
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(encoded_jwt):
    return jwt.decode(encoded_jwt, SECRET_KEY, algorithms=[ALGORITHM])