from fastapi import APIRouter
from app.schemas import *

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/registration", response_model=UserRegisterOut)
def penis(registration: UserRegisterIn):
    return registration
