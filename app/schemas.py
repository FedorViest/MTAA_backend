from pydantic import BaseModel


class UserRegisterIn(BaseModel):
    name: str
    password: str
    username: str
    email: str


class UserRegisterOut(BaseModel):
    name: str
    username: str
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


class AllRatingsOut(BaseModel):
    id: int
    rating: float
    comment: str

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
