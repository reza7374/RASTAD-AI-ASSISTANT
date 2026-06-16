from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.message_schema import MessageRequest, MessageReplyResponse
from app.services.message_service import message_service
import traceback

router = APIRouter(prefix="/message", tags=["Message"])


@router.post("/", response_model=MessageReplyResponse)
def handle_message(request: MessageRequest, db: Session = Depends(get_db)):
    try:
        return message_service.handle_message(
            db=db,
            user_id=request.user_id,
            name=request.name,
            message=request.message
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
