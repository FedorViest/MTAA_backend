from fastapi import APIRouter, Depends

from app.models import Users
from app.schemas.users import *
from app.database import connect_to_db
from sqlalchemy.orm import Session
from app.utils import *

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



