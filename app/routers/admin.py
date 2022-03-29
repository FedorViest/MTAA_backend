from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app import oauth
from app.schemas.admin import *
from app.database import connect_to_db
from sqlalchemy.orm import Session, aliased
from app.models import *
from app.utils import pwd_context
import app.utils as utils
from sqlalchemy import and_

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/getRatings", response_model=List[AllRatingsOut], summary="Get all ratings")
def all_ratings(db_conn: Session = Depends(connect_to_db), current_user: Users = Depends(oauth.get_user)):
    """
      Get a list of all the ratings with this information in a response body:

     - **id**: every rating has a unique id
     - **customer_name**: every rating has a customer that posted it
     - **employee_name**: every rating has a target employee
     - **rating**: every rating has a floating number of stars
     - **comment**: every rating has a customer's comment
      """

    utils.validate_user(current_user, "admin")

    user_employee = aliased(Users)
    user_customer = aliased(Users)

    result = db_conn.query(Ratings, user_employee.email.label("employee_email"),
                           user_customer.email.label("customer_email")).\
        join(user_customer, user_customer.id == Ratings.customer_id).\
        join(user_employee, user_employee.id == Ratings.employee_id).\
        all()

    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No ratings found")

    return result


@router.post("/addEmployee", response_model=AddEmployeeOut, summary="Add new employee to the database")
def post_employee(employee_details: AddEmployeeIn, db_conn: Session = Depends(connect_to_db),
                  current_user: Users = Depends(oauth.get_user)):
    """
    Create a new employee with this information required to be present in a request body:

    - **name**: every new employee has to have a name
    - **password**: every employee has to have a password
    - **email**: every employee has to have a unique email address
    - **position**: every employee has to have a position (either employee or admin)
    - **skills**: every employee has a set of skills

    This API call returns this information in a response body:

    - **name**: new employee's name
    - **email**: new employee's unique email
      """

    utils.validate_user(current_user, "admin")

    hashed_password = pwd_context.hash(employee_details.password)
    employee_details.password = hashed_password

    result_query = db_conn.query(Users).filter(Users.email == employee_details.email)

    if result_query.first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Employee with selected email already exists")

    new_user = Users(**employee_details.dict())

    db_conn.add(new_user)
    db_conn.commit()
    db_conn.refresh(new_user)

    return new_user


@router.post("/addComputer", response_model=AddComputerOut, summary="Add new computer to the database")
def post_computer(computer_details: AddComputerIn, db_conn: Session = Depends(connect_to_db),
                  current_user: Users = Depends(oauth.get_user)):

    """
    Create a new computer with this information required to be present in a request body:

    - **brand**: every computer has its own brand
    - **model**: every brand has a model
    - **year_made**: every computer has a year in which it has been published

    This API call returns this information in a response body:

    - **brand**: every computer has its own brand
    - **model**: every brand has a model
    - **year_made**: every computer has a year in which it has been published
      """

    utils.validate_user(current_user, "admin")

    new_computer = Computers(**computer_details.dict())

    db_conn.add(new_computer)
    db_conn.commit()
    db_conn.refresh(new_computer)

    return new_computer


@router.get("/getComputers", response_model=List[GetComputersOut], summary="Get all computers")
def get_computers(db_conn: Session = Depends(connect_to_db), current_user: Users = Depends(oauth.get_user)):
    """
    Get a list of all the ratings with this information in a response body:

    - **brand**: every computer has its own brand
    - **model**: every brand has a model
    - **year_made**: every computer has a year in which it has been published
      """

    utils.validate_user(current_user, "admin")

    result = db_conn.query(Computers).all()

    return result


@router.put("/changeEmployee/{email}", response_model=UpdateEmployeeOut, summary="Change employee' information")
def change_employee(employee_info: UpdateEmpolyeeIn, db_conn: Session = Depends(connect_to_db),
                    current_user: Users = Depends(oauth.get_user)):

    """
    Change information about employee based on these parameters:

    - **email**: email of the employee that is to be updated

    This information is required to be present in a request body:

    - **name**: every employee has to have a name
    - **password**: every employee has to have a password
    - **email**: every employee has to have a unique email
    - **skills**: every employee has a set of skills

    This API call returns this information in a response body:

    - **name**: new name of employee
    - **email**: new email of employee
    - **skills**: new skills of employee
      """

    utils.validate_user(current_user, "admin")

    query_result = db_conn.query(Users).filter(and_(Users.email == employee_info.email,
                                                    Users.position == 'technician'))

    if not query_result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    query_result.update(employee_info.dict())
    db_conn.commit()

    return employee_info.dict()


@router.delete("/deleteEmployee/{email}", status_code=status.HTTP_200_OK, summary="Delete employee from the database")
def delete_employee(email, db_conn: Session = Depends(connect_to_db),
                    current_user: Users = Depends(oauth.get_user)):

    """
    Delete employee from the database with these parameters:

    - **email**: email of the employee that is going to be deleted
    """

    utils.validate_user(current_user, "admin")

    result_query = db_conn.query(Users).filter(Users.email == email)

    if not result_query.first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Selected employee does not exist")

    result_query.delete()
    db_conn.commit()

    return status.HTTP_200_OK


@router.put("/assignEmployee/{email}/{order_id}", response_model=UpdateOrderOut, summary="Assign employee a repair")
def assign_employee(email: str, order_id: int, db_conn: Session = Depends(connect_to_db),
                    current_user: Users = Depends(oauth.get_user)):

    """
    Delete employee from the database with these parameters:

    - **email**: email of the employee that is going to be assigned to the order
    - **order_id**: order's id that is going to be assigned to the employee
    """

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
