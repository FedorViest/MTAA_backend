import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, validator


class UserLoginIn(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class getInfoOut(BaseModel):
    name: str
    email: str
    registration_date: datetime.date
    position: str
    skills: Optional[str]

    class Config:
        orm_mode = True
