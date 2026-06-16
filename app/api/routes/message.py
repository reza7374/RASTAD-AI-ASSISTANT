from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.message_schema import MessageRequest, MessageResponse
from app.services.message_service import message_service

router = APIRouter(prefix="/message", tags=["Message"])


@router.post("/", response_model=MessageResponse)
def handle_message(
    request: MessageRequest,
    db: Session = Depends(get_db),
):
    """
    Main endpoint for receiving user messages.
    """

    try:
        response = message_service.handle_message(
            db=db,
            user_id=request.user_id,
            name=request.name,
            message=request.message,
        )

        return response

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing message."
        )
