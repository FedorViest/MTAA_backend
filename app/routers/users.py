from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app import utils, oauth
from app.models import Users
from app.schemas.users import *
from app.database import connect_to_db
from sqlalchemy.orm import Session
from app.utils import *

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# get_current_user: int = Depends(oauth.get_user)

@router.post("/login")
def login(user_login_info: OAuth2PasswordRequestForm = Depends(), db_conn: Session = Depends(connect_to_db)):
    print(user_login_info.username)

    user = db_conn.query(Users).filter(Users.email == user_login_info.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login details")

    if not utils.password_check(user_login_info.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login details")

    access_token = oauth.create_token(data={"id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/getInfo", response_model=getInfoOut)
def get_current_user_info(db_conn: Session = Depends(connect_to_db), current_user: Users = Depends(oauth.get_user)):

    user = db_conn.query(Users).filter(Users.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return user


@router.get("/getInfo/{email}", response_model=getInfoOut)
def get_user_info(email, db_conn: Session = Depends(connect_to_db), current_user: Users = Depends(oauth.get_user)):

    user = db_conn.query(Users).filter(Users.email == email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return user
