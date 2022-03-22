from fastapi import APIRouter, Depends
from app.schemas import *
from app.database import connect_to_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/getRatings", response_model=AllRatingsOut)
def all_ratings(conn_db: Session = Depends(connect_to_db)):
    # TODO - query
    return None
