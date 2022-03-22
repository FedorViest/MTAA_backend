from fastapi import APIRouter, Depends
from app.schemas import *
from app.database import connect_to_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/customer",
    tags=["Customer"]
)


@router.get("/getOrders", response_model=OrdersOut)
def all_orders(conn_db: Session = Depends(connect_to_db)):
    # TODO - query
    return None


@router.get("/getOrders/{id}", response_model=OrdersOut)
def display_order(order: OneOrderIn):
    # TODO - query
    return None
