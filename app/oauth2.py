from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import database
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# HEAD{ALGORITHM AND TYPE},PAYLOAD{USERS INFO},SIGNATURE{HEAD+PAYLOAD+SECRET}

# SECRET_KEY
# PAYLOAD DATA
# ALGORITHM
# EXPIRATION DATE

SECRETE_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minute


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# verify token


def verify_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])
        token_id: str = payload.get("user_id")
        current_user_id = schemas.TokenData(id=token_id)
        if not token_id:
            raise credential_exception

    except JWTError:
        raise credential_exception
    return current_user_id


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="log-in Expired... log in again", headers={"www-Authenticate": "Bearer"})
    token = verify_token(token, credential_exception)
    query_token = db.query(models.ORM_User).filter(
        models.ORM_User.id == token.id)
    user = query_token.first()
    return user


# detail="could not validate credentials",headers={"www-Authenticate": "Bearer"}
