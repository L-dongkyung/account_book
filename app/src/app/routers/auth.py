from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt
from pydantic import ValidationError

from db import db
from config import Config
from models.user import User
from schemas.token_schema import TokenPayload


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"api/v1/login/access-token"
)


def get_current_user(session: Session = Depends(db.get_db), token: str = Depends(reusable_oauth2)) -> User:
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = User.get(session, email=token_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
