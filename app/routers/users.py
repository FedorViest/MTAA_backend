from fastapi import APIRouter
from app.schemas import *

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/registration", response_model=UserRegisterOut)
def penis(registration: UserRegisterIn):
    return registration


@router.get("/login", response_model=UserLoginOut)
def user_login(login_details: UserLoginIn):
    return login_details
