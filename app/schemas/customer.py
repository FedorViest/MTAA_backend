import datetime

from pydantic import BaseModel


class UserRegisterIn(BaseModel):
    name: str
    password: str
    email: str
    position: str = "customer"


class UserRegisterOut(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class UserLoginIn(BaseModel):
    username: str
    password: str


class UserLoginOut(BaseModel):
    username: str

    class Config:
        orm_mode = True


class OrdersOut(BaseModel):
    id: int
    state: str
    problem: str

    class Config:
        orm_mode = True


class OneOrderIn(BaseModel):
    id: int


class AddOrderIn(BaseModel):
    customer_email: str
    employee_email: str
    pc_brand: str
    pc_model: str
    pc_year: int
    status: str = "accepted"
    issue: str


class AddOrderOut(BaseModel):
    customer_email: str
    status: str


    class Config:
        orm_mode = True


class GetOrderIn(BaseModel):
    id: int


class GetOrderOut(BaseModel):
    id: int
    status: str
    date_created: datetime.datetime
    issue: str

    class Config:
        orm_mode = True


class EmployeeNameOut(BaseModel):
    Orders: GetOrderOut
    employee_name: str

    class Config:
        orm_mode = True
