import datetime

from pydantic import BaseModel, EmailStr


class AllRatingsOut(BaseModel):
    id: int
    rating: float
    comment: str

    class Config:
        orm_mode = True


class RatingsOut(BaseModel):
    Ratings: AllRatingsOut
    employee_email: str
    customer_email: str

    class Config:
        orm_mode = True


class AddEmployeeIn(BaseModel):
    name: str
    password: str
    email: EmailStr
    position: str
    skills: str


class AddEmployeeOut(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class AddComputerIn(BaseModel):
    brand: str
    model: str
    year_made: str


class AddComputerOut(BaseModel):
    brand: str
    model: str
    year_made: str

    class Config:
        orm_mode = True


class GetComputersOut(BaseModel):
    id: int
    brand: str
    model: str
    year_made: str

    class Config:
        orm_mode = True


class UpdateEmpolyeeIn(BaseModel):
    name: str
    email: EmailStr
    skills: str


class UpdateEmployeeOut(BaseModel):
    name: str
    email: str
    skills: str

    class Config:
        orm_mode = True


class UpdateOrderOut(BaseModel):
    id: int
    customer_id: int
    employee_id: int
    status: str
    issue: str

    class Config:
        orm_mode = True

class AllEmployeesOut(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True

class OrderOut(BaseModel):
    id: int
    status: str
    date_created: datetime.date
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
    user_email: str

    class Config:
        orm_mode = True
