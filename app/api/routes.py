from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

router = APIRouter()


@router.get("/db-test")
def test_db(db: Session = Depends(get_db)):
    return {"message": "database session works"}



from app.schemas.message_schema import MessageRequest, MessageResponse
from app.services.message_service import handle_message

router = APIRouter()


@router.post("/message", response_model=MessageResponse)
def message_endpoint(request: MessageRequest, db: Session = Depends(get_db)):
    return handle_message(request, db)
