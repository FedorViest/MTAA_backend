from fastapi import APIRouter, Depends
from app.schemas import *
from app.database import connect_to_db
from sqlalchemy.orm import Session
from app.utils import *
from app.models import *

router = APIRouter(
    prefix="/customer",
    tags=["Customer"]
)


@router.post("/registration", response_model=UserRegisterOut)
def register(user_credentials: UserRegisterIn, db_conn: Session = Depends(connect_to_db)):
    hashed_password = pwd_context.hash(user_credentials.password)
    user_credentials.password = hashed_password

    new_user = Users(**user_credentials.dict())

    db_conn.add(new_user)
    db_conn.commit()
    db_conn.refresh(new_user)

    user_id = db_conn.query(Users.id).filter(Users.email == user_credentials.email).scalar()

    new_customer = Customers(users_id=user_id)

    db_conn.add(new_customer)
    db_conn.commit()
    db_conn.refresh(new_customer)

    return new_user


@router.get("/getOrders", response_model=OrdersOut)
def all_orders(conn_db: Session = Depends(connect_to_db)):
    # TODO - query
    return None


@router.get("/getOrders/{id}", response_model=OrdersOut)
def display_order(order: OneOrderIn):
    # TODO - query
    return None
