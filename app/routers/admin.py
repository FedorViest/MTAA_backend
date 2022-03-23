from typing import List

from fastapi import APIRouter, Depends
from app.schemas.admin import *
from app.database import connect_to_db
from sqlalchemy.orm import Session
from app.models import *
from app.utils import pwd_context

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/getRatings", response_model=AllRatingsOut)
def all_ratings(db_conn: Session = Depends(connect_to_db)):
    result = db_conn.query(Ratings).all()

    return result
