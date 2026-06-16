# app/api/router.py

from fastapi import APIRouter

from app.api.routes import message

api_router = APIRouter()

api_router.include_router(message.router)
