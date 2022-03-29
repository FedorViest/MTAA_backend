import base64
import os
import io
import numpy as np
from fastapi import APIRouter, Depends, status, HTTPException, Response, UploadFile, File
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from starlette.responses import StreamingResponse
import cv2

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

@router.post("/login", summary="Logs in existing user")
def login(user_login_info: OAuth2PasswordRequestForm = Depends(), db_conn: Session = Depends(connect_to_db)):

    """
        Required request body:

        -**email**: email of user
        -**password**: password of user

        This API call returns access token
    """

    user = db_conn.query(Users).filter(Users.email == user_login_info.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login details")

    if not utils.password_check(user_login_info.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login details")

    access_token = oauth.create_token(data={"id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/getInfo", response_model=getInfoOut, summary="Displays information about logged in user")
def get_current_user_info(db_conn: Session = Depends(connect_to_db), current_user: Users = Depends(oauth.get_user)):
    """
            Required response body:

            - **name**: name of logged in user
            - **email**: email of logged in user
            - **registration_date**: date, when logged in user was registered
            - **position**: position of logged in user(customer/employee/admin)
            - **skills [Optional]**: skills when logged in user is employee
        """

    user = db_conn.query(Users).filter(Users.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return user


@router.get("/getInfo/{email}", response_model=getInfoOut, summary="Displays information about user with given email")
def get_user_info(email, db_conn: Session = Depends(connect_to_db), current_user: Users = Depends(oauth.get_user)):
    """
                Required parameter:

                - **email**: email of user, whose information should be displayed

                Required response body:

                - **name**: name of selected user
                - **email**: email of selected user
                - **registration_date**: date, when selected user was registered
                - **position**: position of selected user(customer/employee/admin)
                - **skills [Optional]**: skills when selected user is employee
            """

    if not utils.email_valid(email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid email")

    user = db_conn.query(Users).filter(Users.email == email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return user


@router.post("/uploadPicture", summary="Uploads picture from folder")
async def upload_picture(image: UploadFile = File(...), db_conn: Session = Depends(connect_to_db),
                   current_user: Users = Depends(oauth.get_user)):

    """
        Required request body:
        - **image**: image selected from computer

        Required response body:
        - **"Upload image": "Successful"**

    """

    path = "app/pictures/" + image.filename

    data = cv2.imread(path)
    data_resized = cv2.resize(data, (100, 100))
    result, encoded_image = cv2.imencode(".png", data_resized)

    result_query = db_conn.query(Users).filter(Users.id == current_user.id)

    result_query.update({"profile_pic": encoded_image})
    db_conn.commit()

    return {"Upload image": "Successful"}


@router.get("/getPicture", summary="Get profile picture of logged in user")
async def get_picture(db_conn: Session = Depends(connect_to_db), current_user: Users = Depends(oauth.get_user)):

    """
        Required response body:

        - **image**: in png format
    """

    result_query = db_conn.query(Users).filter(Users.id == current_user.id).first()

    if not result_query:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Unknown user")

    image = result_query.profile_pic

    img = np.asarray(bytearray(image), dtype="uint8")

    return StreamingResponse(io.BytesIO(img.tobytes()), media_type="image/png")
