from fastapi import APIRouter

from app.user.api_v1 import router as user_router

api_router_v1 = APIRouter()
api_router_v1.include_router(user_router, prefix="/users", tags=["users"])
