from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_
from starlette import status

from app.schemas.employee import *
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


@router.put("/updateOrderState/{order_id}", response_model=updateOrderStateOut)
def update_order(order_info: updateOrderStateIn, order_id: int, db_conn: Session = Depends(connect_to_db),
                 current_user: Users = Depends(oauth.get_user)):
    utils.validate_user(current_user, "employee")

    query_result = db_conn.query(Orders).filter(Orders.id == order_id)

    if not query_result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Order not found")

    query_result.update(order_info.dict())
    db_conn.commit()

    return order_info.dict()


@router.get("/getRepairs", response_model=List[getRepairsOut])
def get_repairs(db_conn: Session = Depends(connect_to_db), current_user: Users = Depends(oauth.get_user)):
    utils.validate_user(current_user, "employee")

    query_result = db_conn.query(Orders).filter(current_user.id == Orders.employee_id).all()

    if not query_result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="You do not have any repairs")

    return query_result


@router.get("/getRepairs/{repair_id}", response_model=RepairOut)
def get_repair(repair_id: int, db_conn: Session = Depends(connect_to_db),
               current_user: Users = Depends(oauth.get_user)):

    utils.validate_user(current_user, "employee")

    query_result = db_conn.query(Orders, Computers.brand, Computers.model, Computers.year_made).\
        join(Computers, Orders.pc_id == Computers.id).\
        filter(and_(repair_id == Orders.id, current_user.id == Orders.employee_id)).first()

    if not query_result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="You do not have any repairs")

    return query_result
