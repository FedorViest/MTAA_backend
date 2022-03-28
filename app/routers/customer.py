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

    result_query = db_conn.query(Users).filter(Users.email == user_credentials.email)

    if result_query:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User with selected email already exists")

    new_user = Users(**user_credentials.dict())

    db_conn.add(new_user)
    db_conn.commit()
    db_conn.refresh(new_user)

    return new_user


@router.get("/getOrders", response_model=List[OrdersOut])
def all_orders(db_conn: Session = Depends(connect_to_db), current_user: Users = Depends(oauth.get_user)):

    validate_user(current_user, "customer")

    db_conn.query(Orders)

    query_result = db_conn.query(Orders).filter(current_user.id == Orders.customer_id).all()

    if not query_result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="You do not have any orders")

    return query_result


@router.post("/addOrder")
def post_order(order_details: AddOrderIn, db_conn: Session = Depends(connect_to_db),
               current_user: Users = Depends(oauth.get_user)):

    validate_user(current_user, "customer")

    customer_id = db_conn.query(Users.id).filter(and_(Users.email == order_details.customer_email,
                                                      Users.position == "customer")).first()

    employee_id = db_conn.query(Users.id).filter(and_(Users.email == order_details.employee_email,
                                                      Users.position == "employee")).first()

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


@router.get("/getOrders/{order_id}", response_model=EmployeeNameOut)
def get_orders(order_id: int, db_conn: Session = Depends(connect_to_db),
               current_user: Users = Depends(oauth.get_user)):
    validate_user(current_user, "customer")

    user_employee = aliased(Users)
    user_customer = aliased(Users)

    query_result = db_conn.query(Orders, Computers, user_employee.name.label("employee_name"),
                                 user_customer.email.label("user_email")). \
        join(Computers, Computers.id == Orders.pc_id). \
        join(user_employee, user_employee.id == Orders.employee_id, isouter=True). \
        join(user_customer, user_customer.id == Orders.customer_id). \
        filter(and_(Orders.id == order_id, current_user.id == Orders.customer_id)).first()

    if not query_result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Order not found")

    print(query_result)

    return query_result


@router.post("/addRating", response_model=AddRatingOut)
def post_rating(rating_details: AddRatingIn, db_conn: Session = Depends(connect_to_db),
                current_user: Users = Depends(oauth.get_user)):

    validate_user(current_user, "customer")

    customer_id = db_conn.query(Users.id).filter(and_(Users.email == current_user.email,
                                                      Users.position == "customer")).first()

    employee_id = db_conn.query(Users.id).filter(and_(Users.email == rating_details.employee_email,
                                                      Users.position == "employee")).first()

    if not employee_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Incorrect technician assigned")

    customer_id = customer_id["id"]
    employee_id = employee_id["id"]

    new_rating = Ratings(customer_id=customer_id, employee_id=employee_id, rating=rating_details.rating_stars,
                         comment=rating_details.comment)

    db_conn.add(new_rating)
    db_conn.commit()
    db_conn.refresh(new_rating)

    return new_rating


@router.delete("/removeRating/{rating_id}")
def remove_rating(rating_id: int, db_conn: Session = Depends(connect_to_db),
                  current_user: Users = Depends(oauth.get_user)):

    validate_user(current_user, "customer")

    result_query = db_conn.query(Ratings).filter(and_(Ratings.id == rating_id, Ratings.customer_id == current_user.id))

    if not result_query:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Incorrect rating details")

    result_query.delete()
    db_conn.commit()

    return f"Successfully deleted rating id: {rating_id}", status.HTTP_200_OK
