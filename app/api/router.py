# app/api/router.py

from fastapi import APIRouter

from app.api.routes import message, user

api_router = APIRouter()

api_router.include_router(message.router)

api_router.include_router(user.router, prefix="/management")
