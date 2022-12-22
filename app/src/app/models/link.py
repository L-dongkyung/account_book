from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship

from models.crud import BaseCRUD
from db import Base


# DB Model
class Link(Base, BaseCRUD):
    __tablename__ = 'link'
    detail_id = Column(Integer, ForeignKey('detail.id'), nullable=False, index=True)
    ttl = Column(Integer)
    link_hash = Column(String(length=255), index=True)
    detail = relationship("Detail")
