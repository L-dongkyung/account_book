from pydantic import BaseModel


class LinkInDB(BaseModel):
    id: int
    link_hash: str
    detail_id: int
    ttl: int

    class Config:
        orm_mode = True


class CreateLink(BaseModel):
    detail_id: int
    ttl: int = None
