from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app import oauth
from app.schemas.admin import *
from app.database import connect_to_db
from sqlalchemy.orm import Session
from app.models import *
from app.utils import pwd_context
import app.utils as utils
from sqlalchemy import and_

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# current_user: int = Depends(oauth.get_user)


@router.get("/getRatings", response_model=AllRatingsOut)
def all_ratings(db_conn: Session = Depends(connect_to_db), current_user: Users = Depends(oauth.get_user)):
    utils.validate_user(current_user, "admin")

    result = db_conn.query(Ratings).all()

    return result


@router.post("/addEmployee", response_model=AddEmployeeOut)
def post_employee(employee_details: AddEmployeeIn, db_conn: Session = Depends(connect_to_db),
                  current_user: Users = Depends(oauth.get_user)):
    utils.validate_user(current_user, "admin")

    hashed_password = pwd_context.hash(employee_details.password)
    employee_details.password = hashed_password

    # print("Email:" + current_user.email + " Position:" + current_user.position)

    result_query = db_conn.query(Users).filter(Users.email == employee_details.email)

    if result_query.first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Employee with selected email already exists")

    new_user = Users(**employee_details.dict())

    db_conn.add(new_user)
    db_conn.commit()
    db_conn.refresh(new_user)

    return new_user


@router.post("/addComputer", response_model=AddComputerOut)
def post_computer(computer_details: AddComputerIn, db_conn: Session = Depends(connect_to_db),
                  current_user: Users = Depends(oauth.get_user)):
    utils.validate_user(current_user, "admin")

    new_computer = Computers(**computer_details.dict())

    db_conn.add(new_computer)
    db_conn.commit()
    db_conn.refresh(new_computer)

    return new_computer


@router.get("/getComputers", response_model=List[GetComputersOut])
def get_computers(db_conn: Session = Depends(connect_to_db), current_user: Users = Depends(oauth.get_user)):
    utils.validate_user(current_user, "admin")

    result = db_conn.query(Computers).all()

    return result


@router.put("/changeEmployee/{email}", response_model=UpdateEmployeeOut)
def change_employee(employee_info: UpdateEmpolyeeIn, db_conn: Session = Depends(connect_to_db),
                    current_user: Users = Depends(oauth.get_user)):
    utils.validate_user(current_user, "admin")

    query_result = db_conn.query(Users).filter(and_(Users.email == employee_info.email,
                                                    Users.position == 'technician'))

    if not query_result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    query_result.update(employee_info.dict())
    db_conn.commit()

    return employee_info.dict()


@router.delete("/deleteEmployee/{email}", status_code=status.HTTP_200_OK)
def delete_employee(email, db_conn: Session = Depends(connect_to_db),
                    current_user: Users = Depends(oauth.get_user)):
    utils.validate_user(current_user, "admin")

    result_query = db_conn.query(Users).filter(Users.email == email)

    if not result_query.first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Selected employee does not exist")

    result_query.delete()
    db_conn.commit()

    return status.HTTP_200_OK


@router.put("/assignEmployee/{email}/{order_id}", response_model=UpdateOrderOut)
def assign_employee(email: str, order_id: int, db_conn: Session = Depends(connect_to_db),
                    current_user: Users = Depends(oauth.get_user)):
    utils.validate_user(current_user, "admin")

    result_query_employees = db_conn.query(Users.id).filter(and_(Users.email == email,
                                                                 Users.position == "employee"))

    query_check = result_query_employees.first()

    if not query_check:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Specified order or email not found')

    result_query_orders = db_conn.query(Orders).filter(Orders.id == order_id)

    query_check = result_query_orders.first()

    if not query_check:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Specified order or email not found')

    result = result_query_orders.first()

    result_query_orders.update({"employee_id": result_query_employees})

    db_conn.commit()

    return result
