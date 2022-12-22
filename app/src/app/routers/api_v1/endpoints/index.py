from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from db import db
from routers.auth import get_current_user
from models.user import User
from schemas import user_schema

router = APIRouter()


@router.get("/")
async def index(session: Session = Depends(db.session)) -> Response:
    """
    index 확인용 API.
    """
    current_time = datetime.utcnow()
    return Response(f"fast api normal (UTC: {current_time}, DB_version: {session})", status_code=200)


@router.get("/me/", response_model=user_schema.User)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    토큰을 통해서 현재 사용자의 정보를 가져오는 API.
    :param current_user: 현재 user.
    :return: user
    """
    return current_user
