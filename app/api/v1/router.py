from fastapi import APIRouter
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.user import router as user_router
from app.api.v1.endpoints.link import router as link_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(link_router)
