from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship

from models.crud import BaseCRUD
from db import Base
from models.detail import Detail


# DB Model
class Receipt(Base, BaseCRUD):
    __tablename__ = 'receipt'
    user_id = Column(Integer,  ForeignKey('user.id'), nullable=False, index=True)
    payment = Column(Integer)
    store = Column(String(length=255))
    memo = Column(String(length=255))
    details = relationship("Detail", back_populates="receipt")
    user = relationship("User", back_populates="receipts", uselist=False)
