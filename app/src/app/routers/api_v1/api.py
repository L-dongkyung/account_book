from fastapi import APIRouter

from routers.api_v1.endpoints import index, user, login, receipt, detail

api_router = APIRouter(
    prefix="/api/v1"
)

api_router.include_router(index.router, tags=["index"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(receipt.router, prefix="/receipt", tags=["receipt"])
api_router.include_router(detail.router, prefix="/detail", tags=["detail"])
