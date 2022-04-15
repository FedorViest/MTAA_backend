import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional


class UserRegisterIn(BaseModel):
    name: str
    password: str
    email: EmailStr
    position: str = "customer"


class UserRegisterOut(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class UserLoginIn(BaseModel):
    username: EmailStr
    password: str


class UserLoginOut(BaseModel):
    username: str

    class Config:
        orm_mode = True


class OrdersOut(BaseModel):
    id: int
    status: str
    date_created: datetime.date

    class Config:
        orm_mode = True


class OrderOut(BaseModel):
    id: int
    status: str
    date_created: datetime.datetime
    issue: str

    class Config:
        orm_mode = True


class ComputerOut(BaseModel):
    brand: str
    model: str

    class Config:
        orm_mode = True


class EmployeeNameOut(BaseModel):
    Orders: OrderOut
    Computers: ComputerOut
    employee_email: Optional[str]
    employee_name: Optional[str]
    user_email: str

    class Config:
        orm_mode = True


class AddOrderIn(BaseModel):
    pc_brand: str
    pc_model: str
    pc_year: int
    issue: str


class AddOrderOut(BaseModel):
    customer_email: str
    status: str

    class Config:
        orm_mode = True


class AddRatingIn(BaseModel):
    employee_email: EmailStr
    rating_stars: float
    comment: str


# TODO mozno zmenit id na email
class AddRatingOut(BaseModel):
    customer_id: str
    employee_id: str
    rating: float
    comment: str

    class Config:
        orm_mode = True
