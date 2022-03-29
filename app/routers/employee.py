from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_
from starlette import status
from app.database import connect_to_db
from sqlalchemy.orm import Session, aliased
from app.models import *
from app.schemas.employee import *
import app.oauth as oauth
import app.utils as utils

router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)


@router.put("/updateOrderState/{order_id}", response_model=updateOrderStateOut, summary="Update state of the order")
def update_order(order_info: updateOrderStateIn, order_id: int, db_conn: Session = Depends(connect_to_db),
                 current_user: Users = Depends(oauth.get_user)):
    """
    Update state of the specified order

    Required parameters:

    - **order_id**: id of the order's state to be updated

    Required request body:

    - **status**: new state of the order

    Required response body:

    - **status**: new state of the order
    """

    utils.validate_user(current_user, "employee")

    query_result = db_conn.query(Orders).filter(Orders.id == order_id)

    if not query_result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Order not found")

    query_result.update(order_info.dict())
    db_conn.commit()

    return order_info.dict()


@router.get("/getRepairs", response_model=List[getRepairsOut], summary="Get all current employee' repairs")
def get_repairs(db_conn: Session = Depends(connect_to_db), current_user: Users = Depends(oauth.get_user)):

    """
    Get list of all repairs for currently signed in employee

    Required response body:

    - **id**: order's id
    - **date_created**: date of order's creation
    - **status**: state of order
    - **issue**: computer's issue specified by the customer
    - **brand**: brand of the computer
    - **model**: model of the computer
    - **year_made**: year in which was the computer published
    - **customer_email**: order's creator (customer) email
    """

    utils.validate_user(current_user, "employee")

    user_customer = aliased(Users)

    result = db_conn.query(Orders, Computers, user_customer.email.label("customer_email")). \
        join(user_customer, user_customer.id == Orders.customer_id). \
        join(Users, current_user.id == Orders.employee_id).\
        join(Computers, Orders.pc_id == Computers.id).\
        all()

    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="You do not have any repairs")

    return result


@router.get("/getRepairs/{repair_id}", response_model=RepairOut, summary="Get specific repair")
def get_repair(repair_id: int, db_conn: Session = Depends(connect_to_db),
               current_user: Users = Depends(oauth.get_user)):
    """
    Get specific repair for currently signed in employee

    Required parameters:
    - **repair_id**: specified order's id

    Required response body:

    - **id**: order's id
    - **status**: order's state
    - **date_created**: order's date of creation
    - **issue**: computer's issue specified by the customer
    - **brand**: brand of the computer
    - **model**: model of the computer
    - **year_made**: year in which was the computer published
    """

    utils.validate_user(current_user, "employee")

    query_result = db_conn.query(Orders, Computers.brand, Computers.model, Computers.year_made).\
        join(Computers, Orders.pc_id == Computers.id).\
        filter(and_(repair_id == Orders.id, current_user.id == Orders.employee_id)).first()

    if not query_result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="You do not have any repairs")

    return query_result
