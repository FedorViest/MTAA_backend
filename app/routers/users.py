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
def login(user_login_info: UserLoginIn, db_conn: Session = Depends(connect_to_db)):

    user = db_conn.query(Users).filter(Users.email == user_login_info.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid login details")

    if not utils.password_check(user_login_info.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid login details")

    access_token = oauth.create_token(data={"id": user.id})

    return {"token": access_token, "token_type": "bearer"}
