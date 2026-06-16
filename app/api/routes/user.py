from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.message_repository import MessageRepository
from app.schemas.user_schema import UserResponse
from app.schemas.message_schema import MessageRecordResponse

router = APIRouter() 

@router.get("/users", response_model=List[UserResponse], tags=["Management"])
def list_users(db: Session = Depends(get_db)):
    return UserRepository.get_all_users(db)

@router.get("/users/{user_id}/messages", response_model=List[MessageRecordResponse], tags=["Management"])
def get_user_history(user_id: str, db: Session = Depends(get_db)):
    user = UserRepository.get_by_user_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return MessageRepository.get_recent_messages(db, user_id)

