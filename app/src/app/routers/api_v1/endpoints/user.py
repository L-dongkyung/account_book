from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from schemas import user_schema
from db import db
from models.user import User
from routers import auth
from config import Config

router = APIRouter()


@router.post("/")
async def create_user(user_info: user_schema.CreateUser, session: Session = Depends(db.get_db)) -> JSONResponse:
    """
    user 생성 API.
    :param user_info: 생성할 유저의 정보.
    :param session: DB 연결 session.
    :return:
    """
    is_exist = await is_email_exist(session, user_info.email)
    if is_exist:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="user is exist")
    if not user_info.email and not user_info.password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="must email and password")
    hashed_pw = Config.pwd_context.hash(user_info.password)
    new_user = User.create(session, auto_commit=True, email=user_info.email, password=hashed_pw)
    return JSONResponse(status_code=200, content=dict(detail=f"user email: {new_user.email} is created"))


async def is_email_exist(session: Session, email: str) -> bool:
    get_email = User.get(session, email=email)
    if get_email:
        return True
    return False


@router.delete("/")
async def delete_user(user: User = Depends(auth.get_current_user), session: Session = Depends(db.get_db)):
    """
    user 삭제 API.
    :param user: 삭제할 유저.
    :param session:
    :return:
    """
    User.filter(session, email=user.email).delete(auto_commit=True)
    return JSONResponse(status_code=200, content=dict(detail=f"user deleted: {user.email}"))
