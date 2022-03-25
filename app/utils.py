from fastapi import HTTPException
from passlib.context import CryptContext
import re

from starlette import status

email_format_regex = '^[a-zA-z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$'

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def email_valid(email: str):
    if re.search(email_format_regex, email):
        return True
    return False


def password_check(password, password_db):
    return pwd_context.verify(password, password_db)


def validate_user(current_user, target_position):
    if current_user.position != target_position:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user for this operation")

