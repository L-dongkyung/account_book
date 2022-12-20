from sqlalchemy import Column, Integer, String, ForeignKey

from models.crud import BaseCRUD
from db import Base


# DB Model
class Detail(Base, BaseCRUD):
    __tablename__ = 'detail'
    receipt_id = Column(Integer,  ForeignKey('receipt.id'), nullable=False, index=True)
    payment_method = Column(String(length=100), nullable=False)
    store_address = Column(String(length=100), nullable=False)
    store_phone = Column(String(length=100), nullable=False)
    store_info = Column(String(length=100), nullable=False)
    url = Column(String(length=100), nullable=False, index=True)
