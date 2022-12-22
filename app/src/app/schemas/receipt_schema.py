from pydantic import BaseModel

from schemas.detail_schema import DetailInDB


class CreateReceipt(BaseModel):
    payment: int
    store: str
    memo: str


class ReceiptInDB(BaseModel):
    id: int
    user_id: int
    payment: int = None
    store: str = None
    memo: str = None

    class Config:
        orm_mode = True


class UpdateReceipt(BaseModel):
    payment: int = None
    memo: str = None
