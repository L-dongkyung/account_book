import time
import hashlib
import base64

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import db
from models.user import User
from models.detail import Detail
from models.link import Link
from routers.auth import get_current_user
from schemas import link_schema, detail_schema

router = APIRouter()


@router.post("/", response_model=link_schema.LinkInDB)
async def create_link(
        link_info: link_schema.CreateLink,
        session: Session = Depends(db.get_db),
        current_user: User = Depends(get_current_user)
):
    """
    link 생성 API.
    :param session:
    :param current_user:
    :return:
    """
    link_data = link_info.dict()
    if Link.filter(session, detail_id=link_data.get("detail_id")).first():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Already exist link")
    detail = Detail.filter(session, id=link_data.get("detail_id")).first()
    if detail.receipt.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid user")
    if link_data.get("ttl", False):
        expires = link_data.get("ttl") * 60 * 60 * 24  # 1 day
    else:
        expires = 60 * 60 * 24 * 7  # 1week
    link_data['ttl'] = time.time() + expires
    link_data['link_hash'] = get_link_hash()
    link = Link.create(session, auto_commit=True, **link_data)
    return link


def get_link_hash():
    md5_hash = hashlib.md5()
    md5_hash.update(bytes(int(time.time())))
    url_hash = base64.urlsafe_b64encode(bytes(md5_hash.digest()))
    return url_hash


@router.get("/{link_hash}", response_model=detail_schema.DetailInDB)
async def get_detail_from_hash(
        link_hash: str,
        session: Session = Depends(db.get_db),
):
    """
    hash를 통해서 detail 정보를 가져올 수 있는 API.
    :param link_hash:
    :param session:
    :return:
    """
    link = Link.get(session, link_hash=link_hash)
    if link.ttl < time.time():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="link expired")
    return link.detail
