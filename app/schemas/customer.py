from pydantic import BaseModel


class UserRegisterIn(BaseModel):
    name: str
    password: str
    email: str


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
