from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.schemas.users import *
from app.database import *
from sqlalchemy.orm import Session
from app.models import *
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users/login')


def create_token(data: dict):
    data_new = data.copy()

    expire_time = datetime.datetime.utcnow() + timedelta(minutes=int(os.getenv("TOKEN_EXPIRE")))
    data_new.update({"exp": expire_time})

    jwt_encoded = jwt.encode(data_new, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

    return jwt_encoded


def verify_token(token: str, cred_exception):
    try:
        decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])

        id: str = decoded_token.get("id")

        if id is None:
            raise cred_exception
        data = TokenData(id=id)

    except JWTError:
        raise cred_exception

    return data


def get_user(token: str = Depends(oauth2_scheme), db_conn: Session = Depends(connect_to_db)):
    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldnt validate credentials",
                                   headers={"WWW-Authenticate": "Bearer"})

    token = verify_token(token, cred_exception)

    user = db_conn.query(Users).filter(Users.id == token.id).first()

    return user
