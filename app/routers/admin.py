from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
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


@router.get("/getRatings", response_model=AllRatingsOut)
def all_ratings(db_conn: Session = Depends(connect_to_db)):
    result = db_conn.query(Ratings).all()

    return result


@router.post("/addEmployee", response_model=AddEmployeeOut)
def post_employee(employee_details: AddEmployeeIn, db_conn: Session = Depends(connect_to_db)):
    hashed_password = pwd_context.hash(employee_details.password)
    employee_details.password = hashed_password

    print(employee_details.email)

    if not utils.email_valid(employee_details.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email")

    new_user = Users(name=employee_details.name, password=employee_details.password, email=employee_details.email)

    db_conn.add(new_user)
    db_conn.commit()
    db_conn.refresh(new_user)

    employee_id = db_conn.query(Users.id).filter(Users.email == employee_details.email).scalar()

    new_employee = Employees(users_id=employee_id, position=employee_details.position, skills=employee_details.skills)

    db_conn.add(new_employee)
    db_conn.commit()
    db_conn.refresh(new_employee)

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
