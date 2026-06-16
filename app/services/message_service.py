from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.repositories.message_repository import MessageRepository
from app.services.intent_service import detect_intent
from app.services.segment_service import detect_segment


def handle_message(request, db: Session):

    user = UserRepository.get_by_user_id(db, request.user_id)

    if not user:
        user = UserRepository.create_user(
            db=db,
            user_id=request.user_id,
            name=request.name
        )

    intent = detect_intent(request.message)

    segment = detect_segment(intent)

    reply = "پاسخ موقت برای MVP"

    needs_human_support = intent == "support_request"

    MessageRepository.create_message(
        db=db,
        user_id=request.user_id,
        user_message=request.message,
        assistant_reply=reply,
        intent=intent,
        needs_human_support=needs_human_support
    )

    return {
        "reply": reply,
        "intent": intent,
        "user_segment": segment,
        "needs_human_support": needs_human_support
    }
