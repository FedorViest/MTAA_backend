from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app import oauth
from app.schemas.customer import *
from app.database import connect_to_db
from sqlalchemy.orm import Session, aliased
from app.utils import *
from app.models import *
from sqlalchemy import and_, func

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

    return new_user


@router.get("/getOrders", response_model=List[EmployeeNameOut])
def all_orders(db_conn: Session = Depends(connect_to_db), current_user: Users = Depends(oauth.get_user)):

    validate_user(current_user, "customer")

    db_conn.query(Orders)

    query_result = db_conn.query(Orders, Users.name.label("employee_name")). \
        join(Users, Users.id == Orders.employee_id, isouter=True). \
        filter(current_user.id == Orders.customer_id).all()

    if not query_result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Order not found")

    return query_result


@router.post("/addOrder")
def post_order(order_details: AddOrderIn, db_conn: Session = Depends(connect_to_db),
               current_user: Users = Depends(oauth.get_user)):

    validate_user(current_user, "customer")

    customer_id = db_conn.query(Users.id).filter(and_(Users.email == order_details.customer_email,
                                                      Users.position == "customer")).first()

    employee_id = db_conn.query(Users.id).filter(and_(Users.email == order_details.employee_email,
                                                      Users.position == "technician")).first()

    pc_id = db_conn.query(Computers.id).filter(and_(Computers.brand == order_details.pc_brand,
                                                    Computers.model == order_details.pc_model,
                                                    Computers.year_made == order_details.pc_year)).first()

    customer_id = customer_id["id"]
    pc_id = pc_id["id"]
    employee_id = employee_id["id"]

    new_order = Orders(customer_id=customer_id, employee_id=employee_id, pc_id=pc_id, status=order_details.status,
                       issue=order_details.issue)

    db_conn.add(new_order)
    db_conn.commit()
    db_conn.refresh(new_order)

    return new_order


@router.post("/getOrders/{order_id}", response_model=EmployeeNameOut)
def get_orders(order_id: int, db_conn: Session = Depends(connect_to_db),
               current_user: Users = Depends(oauth.get_user)):

    validate_user(current_user, "customer")

    query_result = db_conn.query(Orders, Users.name.label("employee_name")).\
        join(Users, Users.id == Orders.employee_id, isouter=True).\
        filter(and_(Orders.id == order_id, current_user.id == Orders.customer_id)).first()

    if not query_result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Order not found")

    print(query_result)

    return query_result
