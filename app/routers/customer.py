from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app import oauth, utils
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


@router.post("/registration", response_model=UserRegisterOut,
             summary="Registers new customer and adds information to database")
def register(user_credentials: UserRegisterIn, db_conn: Session = Depends(connect_to_db)):

    """
    Required request body:

    - **name**: each new user has to have a name
    - **password**: every user has to have a password
    - **email**: every user has to have unique email address
    - **position**: set to default value "customer"

    Required response body:

    - **name**: new users name
    - **email**: new users email
    """

    hashed_password = pwd_context.hash(user_credentials.password)
    user_credentials.password = hashed_password

    if not utils.email_valid(user_credentials.email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid email")

    result_query = db_conn.query(Users).filter(Users.email == user_credentials.email)

    if result_query.first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User with selected email already exists")

    new_user = Users(**user_credentials.dict())

    db_conn.add(new_user)
    db_conn.commit()
    db_conn.refresh(new_user)

    return new_user


@router.get("/getOrders", response_model=List[OrdersOut], summary="List all orders of logged in customer")
def all_orders(db_conn: Session = Depends(connect_to_db), current_user: Users = Depends(oauth.get_user)):

    """
        Required response body:

        - **id**: id of order
        - **status**: status of order (accepted/finished)
        - **date_created**: when was order created

    """

    validate_user(current_user, "customer")

    db_conn.query(Orders)

    query_result = db_conn.query(Orders).filter(current_user.id == Orders.customer_id).order_by(Orders.id).all()

    if not query_result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="You do not have any orders")

    return query_result


@router.post("/addOrder", response_model=AddOrderOut, summary="Creates order with given information")
def post_order(order_details: AddOrderIn, db_conn: Session = Depends(connect_to_db),
               current_user: Users = Depends(oauth.get_user)):
    """
            Required request body:

            - **pc_brand**: brand of computer
            - **pc_model**: model of computer
            - **pc_year**: year computer was made
            - **issue**: what is problem with computer

            Required response body:

            - **customer_email**: email of logged in user
            - **status**: status of order
    """

    validate_user(current_user, "customer")

    customer_id = db_conn.query(Users.id).filter(and_(Users.email == current_user.email,
                                                      Users.position == "customer")).first()

    pc_id = db_conn.query(Computers.id).filter(and_(Computers.brand == order_details.pc_brand,
                                                    Computers.model == order_details.pc_model,
                                                    Computers.year_made == order_details.pc_year)).first()

    customer_id = customer_id["id"]
    pc_id = pc_id["id"]

    new_order = Orders(customer_id=customer_id, employee_id=None, pc_id=pc_id, status="accepted",
                       issue=order_details.issue)

    db_conn.add(new_order)
    db_conn.commit()
    db_conn.refresh(new_order)

    result = {"customer_email": current_user.email,
              "status": "accepted"
              }

    return result


@router.get("/getOrders/{order_id}",
            summary="Returns information about order with given id")
def get_orders(order_id: int, db_conn: Session = Depends(connect_to_db),
               current_user: Users = Depends(oauth.get_user)):
    """
    Required parameters:

    - **order_id**: ID of order

    Required response body:

    - **id**: id of selected order
    - **status**: status of selected order
    - **date_created**: date when order was created
    - **issue**: problem with computer
    - **brand**: brand of computer in order
    - **model**: model of computer in order
    - **employee_name**: name of employee doing the order
    - **user_email**: email of user, who created the repair

    """

    validate_user(current_user, "customer")

    user_employee = aliased(Users)
    user_customer = aliased(Users)

    query_result = db_conn.query(Orders, Computers, user_employee.email.label("employee_email"), user_employee.name.label("employee_name"),
                                 user_customer.email.label("user_email")). \
        join(Computers, Computers.id == Orders.pc_id). \
        join(user_employee, user_employee.id == Orders.employee_id, isouter=True). \
        join(user_customer, user_customer.id == Orders.customer_id). \
        filter(and_(Orders.id == order_id, current_user.id == Orders.customer_id)).first()

    if not query_result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Order not found")

    print(query_result)

    return query_result


@router.post("/addRating", response_model=AddRatingOut, summary="Customer can add rating of selected empolyee")
def post_rating(rating_details: AddRatingIn, db_conn: Session = Depends(connect_to_db),
                current_user: Users = Depends(oauth.get_user)):
    """
        Required request body::

        - **employee_email**: email of employee
        - **rating_stars**: decimal value
        - **comment**: comment of what was positive and/or negative about given employee

        Required response body:

        - **customer_id**: id of logged in customer
        - **employee_id**: id of selected employee
        - **rating** output decimal value
        - **comment**: output comment

    """

    validate_user(current_user, "customer")

    if not utils.email_valid(rating_details.employee_email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid email")

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


@router.get("/getRatings", response_model=List[AllRatingsOut], summary="Returns all ratings of logged in customer")
def get_ratings(db_conn: Session = Depends(connect_to_db),
                current_user: Users = Depends(oauth.get_user)):
    """
    Required response body:

    - **customer_id**: id of logged in customer
    - **employee_id**: id of selected employee
    - **rating** output decimal value
    - **comment**: output comment

    """

    validate_user(current_user, "customer")

    user = aliased(Users)

    query_result = db_conn.query(Ratings, user.email.label("employee_email")). \
        join(user, user.id == Ratings.customer_id). \
        filter(and_(current_user.id == Ratings.customer_id, current_user.position == "customer")).all()

    if not query_result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No ratings found")

    return query_result


@router.delete("/removeRating/{rating_id}", summary="Removes selected rating")
def remove_rating(rating_id: int, db_conn: Session = Depends(connect_to_db),
                  current_user: Users = Depends(oauth.get_user)):

    """
        Required parameter:

        - **rating_id**: id of rating

        Required response body:

        - "Successfully deleted rating id: {rating_id}", status.HTTP_200_OK
    """

    validate_user(current_user, "customer")

    result_query = db_conn.query(Ratings).filter(and_(Ratings.id == rating_id, Ratings.customer_id == current_user.id))

    if not result_query.first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Incorrect rating details")

    result_query.delete()
    db_conn.commit()

    return f"Successfully deleted rating id: {rating_id}", status.HTTP_200_OK


@router.get("/getComputers", response_model=List[GetComputersOut], summary="Get all computers")
def get_computers(db_conn: Session = Depends(connect_to_db), current_user: Users = Depends(oauth.get_user)):
    """
    Get a list of all the ratings

    Required response body:

    - **brand**: every computer has its own brand
    - **model**: every brand has a model
    - **year_made**: every computer has a year in which it has been published
      """

    utils.validate_user(current_user, "customer")

    result = db_conn.query(Computers).all()

    return result