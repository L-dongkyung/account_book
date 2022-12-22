from pydantic import BaseModel


class CreateDetail(BaseModel):
    payment_method: str
    store_address: str = None
    store_phone: str = None
    store_info: str = None


class DetailInDB(BaseModel):
    id: int
    receipt_id: int
    payment_method: str = None
    store_address: str = None
    store_phone: str = None
    store_info: str = None

    class Config:
        orm_mode = True
