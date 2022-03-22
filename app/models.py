from sqlalchemy import Column, Integer, VARCHAR, SmallInteger, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship
# importovat datove typy z SQL
from .database import Base


# ondelete = CASCADE -> foreign key, vymaze sa zaznam
# TIMESTAMP(timezone=True), server_default = text('now()')

class Computers(Base):
    __tablename__ = "computers"

    id = Column(Integer, nullable=False, primary_key=True)
    brand = Column(VARCHAR(50))
    model = Column(VARCHAR(100))
    model_year = Column(SmallInteger)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(VARCHAR(50))
    password = Column(VARCHAR)
    email = Column(VARCHAR(50))
    username = Column(VARCHAR(15))
    role = Column(VARCHAR(8))
    registration_date = Column(TIMESTAMP(timezone=True), server_default=text('now()'))


class Customers(Base):
    __tablename__ = "customers"

    id = Column(Integer, nullable=False, primary_key=True)
    users_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


class Employees(Base):
    __tablename__ = "employees"

    id = Column(Integer, nullable=False, primary_key=True)
    users_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
