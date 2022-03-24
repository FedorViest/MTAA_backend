from pydantic import BaseModel


class AllRatingsOut(BaseModel):
    id: int
    rating: float
    comment: str

    class Config:
        orm_mode = True


class AddEmployeeIn(BaseModel):
    name: str
    password: str
    email: str
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
    brand: str
    model: str
    year_made: str

    class Config:
        orm_mode = True


class UpdateEmpolyeeIn(BaseModel):
    name: str
    password: str
    email: str
    skills: str


class UpdateEmployeeOut(BaseModel):
    name: str
    email: str
    skills: str

    class Config:
        orm_mode = True
