from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from db import db
from routers.auth import get_current_user
from models.user import User
from models.receipt import Receipt
from models.detail import Detail
from schemas import receipt_schema
from schemas import detail_schema


router = APIRouter()


@router.post("/", response_model=receipt_schema.ReceiptInDB)
async def create_receipt(
        receipt_info: receipt_schema.CreateReceipt,
        detail_info: detail_schema.CreateDetail,
        session: Session = Depends(db.get_db),
        current_user: User = Depends(get_current_user)
):
    """
    receipt를 생성하는 API.
    :param receipt_info: receipt 정보
    :param detail_info: detail 정보
    :param session:
    :param current_user: token을 통한 receipt, detail 생성 유저.
    :return:
    """
    try:
        receipt_data = jsonable_encoder(receipt_info)
        receipt = Receipt.create(session, auto_commit=True, **receipt_data, user_id=current_user.id)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed create receipt")
    try:
        detail_data = jsonable_encoder(detail_info)
        Detail.create(session, auto_commit=True, **detail_data, receipt_id=receipt.id)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed create detail")
    return receipt


@router.put("/{receipt_id}", response_model=receipt_schema.ReceiptInDB)
async def update_receipt(
        receipt_id: int,
        receipt_info: receipt_schema.UpdateReceipt,
        session: Session = Depends(db.get_db),
        current_user: User = Depends(get_current_user)
):
    """
    receipt를 수정하는 API.
    :param receipt_id: 경로에 id 값
    :param receipt_info: 수정하려는 데이터
    :param session:
    :param current_user:
    :return:
    """
    update_data = receipt_info.dict(exclude_none=True)
    Receipt.filter(session, id=receipt_id, user_id=current_user.id).update(auto_commit=True, **update_data)
    return Receipt.get(id=receipt_id)


@router.delete("/{receipt_id}")
async def delete_receipt(
        receipt_id: int,
        session: Session = Depends(db.get_db),
        current_user: User = Depends(get_current_user)
):
    """
    receipt 삭제 API.
    :param receipt_id:
    :param session:
    :param current_user:
    :return:
    """
    Receipt.filter(session, id=receipt_id, user_id=current_user.id).delete(auto_commit=True)
    return JSONResponse(status_code=status.HTTP_200_OK, content=dict(detail=f"receipt_id: {receipt_id} is deleted"))


@router.get("/", response_model=list[receipt_schema.ReceiptInDB, ...])
async def list_receipt(
        session: Session = Depends(db.get_db),
        current_user: User = Depends(get_current_user)
):
    """
    user의 receipt 조회.
    :param session:
    :param current_user:
    :return:
    """
    receipts = Receipt.filter(session, user_id=current_user.id).all()
    return receipts


@router.get("/{receipt_id}/detail/", response_model=list[detail_schema.DetailInDB, ...])
async def get_detail(
        receipt_id: int,
        session: Session = Depends(db.get_db),
        current_user: User = Depends(get_current_user)
):
    """
    receipt에 대한 detail list 조회 API.
    :param receipt_id:
    :param session:
    :param current_user:
    :return:
    """
    details = Detail.filter(session, receipt_id=receipt_id).all()
    details = [detail for detail in details if detail.receipt.user_id == current_user.id]
    return details

