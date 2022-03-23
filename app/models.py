from sqlalchemy import Column, Integer, VARCHAR, SmallInteger, Float, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from .database import Base


class Computers(Base):
    __tablename__ = "computers"

    id = Column(Integer, nullable=False, primary_key=True)
    brand = Column(VARCHAR(50))
    model = Column(VARCHAR(100))
    year_made = Column(SmallInteger)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(VARCHAR(50))
    password = Column(VARCHAR)
    email = Column(VARCHAR, unique=True)
    registration_date = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'))


class Customers(Base):
    __tablename__ = "customers"

    id = Column(Integer, nullable=False, primary_key=True)
    users_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


class Employees(Base):
    __tablename__ = "employees"

    id = Column(Integer, nullable=False, primary_key=True)
    users_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


class Ratings(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    rating = Column(Float)
    comment = Column(VARCHAR)


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    pc_id = Column(Integer, ForeignKey("computers.id"), nullable=False)
    date = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'))
    status = Column(VARCHAR(20))
    issue = Column(VARCHAR(100))
