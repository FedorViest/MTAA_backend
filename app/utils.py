from fastapi import HTTPException
from passlib.context import CryptContext
import re

from starlette import status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def password_check(password, password_db):
    return pwd_context.verify(password, password_db)


def validate_user(current_user, target_position):
    if current_user.position != target_position:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user for this operation")

