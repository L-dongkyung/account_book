from copy import copy

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import db
from models.user import User
from models.detail import Detail
from routers.auth import get_current_user
from schemas import detail_schema


router = APIRouter()


@router.get("/{detail_id}", response_model=detail_schema.DetailInDB)
async def read_detail(
        detail_id: int,
        session: Session = Depends(db.get_db),
        current_user: User = Depends(get_current_user)
):
    """
    detail 조회 API.
    :param detail_id:
    :param session:
    :param current_user:
    :return:
    """
    detail = Detail.filter(session, id=detail_id).first()
    if detail and detail.receipt.user_id == current_user.id:
        return detail
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid user")


@router.post("/{detail_id}", response_model=detail_schema.DetailInDB)
async def copy_detail(
        detail_id: int,
        session: Session = Depends(db.get_db),
        current_user: User = Depends(get_current_user)
):
    """
    detail 복사 API.
    :param detail_id:
    :param session:
    :param current_user:
    :return:
    """
    detail = Detail.filter(session, id=detail_id).first()
    if detail and detail.receipt.user_id == current_user.id:
        new_detail_data = copy(detail.__dict__)
        del new_detail_data['id']
        new_detail = Detail.create(session, auto_commit=True, **new_detail_data)
        return new_detail
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="can't copy detail")

