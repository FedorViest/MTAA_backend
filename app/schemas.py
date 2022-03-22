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

    class Config:
        orm_mode = True


class UserLoginOut(BaseModel):
    username: str

    class Config:
        orm_mode = True
