from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app import oauth
from app.schemas.admin import *
from app.database import connect_to_db
from sqlalchemy.orm import Session
from app.models import *
from app.utils import pwd_context
import app.utils as utils


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

# get_current_user: int = Depends(oauth.get_user)


@router.get("/getRatings", response_model=AllRatingsOut)
def all_ratings(db_conn: Session = Depends(connect_to_db)):
    result = db_conn.query(Ratings).all()

    return result


@router.post("/addEmployee", response_model=AddEmployeeOut)
def post_employee(employee_details: AddEmployeeIn, db_conn: Session = Depends(connect_to_db)):
    hashed_password = pwd_context.hash(employee_details.password)
    employee_details.password = hashed_password

    if not utils.email_valid(employee_details.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email")

    new_user = Users(**employee_details.dict())

    db_conn.add(new_user)
    db_conn.commit()
    db_conn.refresh(new_user)

    return new_user


@router.post("/addComputer", response_model=AddComputerOut)
def post_computer(computer_details: AddComputerIn, db_conn: Session = Depends(connect_to_db)):
    new_computer = Computers(**computer_details.dict())

    db_conn.add(new_computer)
    db_conn.commit()
    db_conn.refresh(new_computer)

    return new_computer


@router.get("/getComputers", response_model=List[GetComputersOut])
def get_computers(db_conn: Session = Depends(connect_to_db)):
    result = db_conn.query(Computers).all()

    return result

@router.put("/changeEmployee/{id}")
def change_employee(id, db_conn: Session = Depends(connect_to_db), get_current_user: int = Depends(oauth.get_user)):
    #db_conn.query(User). \
    #    filter(User.username == form.username.data). \
    #    update({'no_of_logins': User.no_of_logins + 1})
    #db_conn.commit()
    return None
