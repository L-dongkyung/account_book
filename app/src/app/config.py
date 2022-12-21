from os import path
from dataclasses import dataclass

from passlib.context import CryptContext


@dataclass
class Config:
    BASE_DIR: str = path.dirname(path.abspath(__file__))  # /app/

    # DB
    DB_URL: str = "mysql+pymysql://root:root@hostname-mysql/payhere?charset=utf8mb4"
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True

    # JWT
    ALGORITHM = "HS256"
    SECRET_KEY = "d363b98d7a437e6b34aa2a45488f3e04f777303b0bb2880d5fe2ac32cb23acd1"  # openssl rand -hex 32
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # crypt
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
