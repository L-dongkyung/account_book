from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship

from models.crud import BaseCRUD
from db import Base


# DB Model
class Receipt(Base, BaseCRUD):
    __tablename__ = 'receipt'
    user_id = Column(Integer,  ForeignKey('user.id'), nullable=False, index=True)
    payment = Column(Integer, nullable=False)
    store = Column(String(length=255), nullable=False)
    memo = Column(String(length=255), nullable=False)
    details = relationship("Detail", back_populates="receipt")
