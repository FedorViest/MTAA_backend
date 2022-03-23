from passlib.context import CryptContext
import re


email_format_regex = '^[a-zA-z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$'


def email_valid(email: str):
    if re.search(email_format_regex, email):
        return True
    return False

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
