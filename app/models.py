from sqlalchemy import Column, Integer, VARCHAR, SmallInteger, Float, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from .database import Base


class Ratings(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Float)
    comment = Column(VARCHAR)


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    pc_id = Column(Integer, ForeignKey("computers.id", ondelete="CASCADE"), nullable=False)
    date = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    status = Column(VARCHAR(20))
    issue = Column(VARCHAR(100))
