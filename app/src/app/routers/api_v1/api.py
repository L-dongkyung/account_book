from fastapi import APIRouter

from routers.api_v1.endpoints import index

api_router = APIRouter(
    prefix="api/v1"
)

api_router.include_router(index.router, tags=["index"])
