from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.crud import BaseCRUD
from db import Base


# DB Model
class Detail(Base, BaseCRUD):
    __tablename__ = 'detail'
    receipt_id = Column(Integer,  ForeignKey('receipt.id'), nullable=False, index=True)
    payment_method = Column(String(length=100))
    store_address = Column(String(length=100))
    store_phone = Column(String(length=100))
    store_info = Column(String(length=100))
    url = Column(String(length=100), index=True)
    receipt = relationship("Receipt", back_populates="details", uselist=False)
