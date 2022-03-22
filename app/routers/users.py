from fastapi import APIRouter, Depends

from app.models import Users
from app.schemas import *
from app.database import connect_to_db
from sqlalchemy.orm import Session
from app.utils import *

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/registration", response_model=UserRegisterOut)
def register(user_credentials: UserRegisterIn, db_conn: Session = Depends(connect_to_db)):
    hashed_password = pwd_context.hash(user_credentials.password)
    user_credentials.password = hashed_password

    new_user = Users(**user_credentials.dict())

    db_conn.add(new_user)
    db_conn.commit()
    db_conn.refresh(new_user)

    return new_user


