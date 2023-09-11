from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security.oauth2 import OAuth2PasswordBearer

from jose import JWTError, jwt
from sqlalchemy.orm import Session


from app.models import models
from app.database import database
from app.schemas import user_schema
from app.config.config import settings


oath2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")
oath2_scheme_admin = OAuth2PasswordBearer(tokenUrl="api/admin")


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    expire = jsonable_encoder(
        datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    data.update({"expiration": expire})

    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: int = payload.get("id")

        if id is None:
            raise credentials_exception

        token_data = user_schema.TokenData(**payload)

    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(
    token: str = Depends(oath2_scheme), db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user







