from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from models.crud import BaseCRUD
from db import Base

from models.receipt import Receipt


# DB Model
class User(Base, BaseCRUD):
    __tablename__ = 'user'
    email = Column(String(length=100), nullable=False, index=True, unique=True)
    password = Column(String(length=100), nullable=False)
    receipts = relationship("Receipt", back_populates="user")

