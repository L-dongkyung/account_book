from pydantic import BaseModel


class CreateUser(BaseModel):
    email: str
    password: str

class User(BaseModel):
    email: str

    class Config:
        orm_mode = True