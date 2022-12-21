from typing import Any
from datetime import timedelta
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt

from db import db
from schemas.token_schema import Token
from models.user import User
from config import Config


router = APIRouter()


@router.post("/access-token", response_model=Token)
async def login_access_token(
    session: Session = Depends(db.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    username(email), password로 access-token 획득.
    """
    user = User.get(session, email=form_data.username)
    if not user or not Config.pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(user.email, expires_delta=access_token_expires),
        "token_type": "bearer",
    }


def create_access_token(
    email: str, expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "email": email}
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt
