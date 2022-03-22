from fastapi import APIRouter, Depends
from app.schemas import *
from app.database import connect_to_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)