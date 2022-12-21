

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from schemas import user_schema
from db import db
from models.user import User

from config import Config

router = APIRouter()


@router.post("/")
async def create_user(user_info: user_schema.CreateUser, session: Session = Depends(db.get_db)):
    is_exist = await is_email_exist(session, user_info.email)
    if is_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user is exist")
    if not user_info.email and not user_info.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="must email and password")
    hashed_pw = Config.pwd_context.hash(user_info.password)
    new_user = User.create(session, auto_commit=True, email=user_info.email, password=hashed_pw)
    return JSONResponse(status_code=200, content=dict(detail=f"user email: {new_user.email} is created"))


async def is_email_exist(session: Session, email: str):
    get_email = User.get(session, email=email)
    if get_email:
        return True
    return False
