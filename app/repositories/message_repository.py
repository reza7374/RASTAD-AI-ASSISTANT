from sqlalchemy.orm import Session

from app.db.models import Message


class MessageRepository:

    @staticmethod
    def create_message(
        db: Session,
        user_id: str,
        user_message: str,
        assistant_reply: str,
        intent: str,
        needs_human_support: bool = False,
    ):
        message = Message(
            user_id=user_id,
            user_message=user_message,
            assistant_reply=assistant_reply,
            intent=intent,
            needs_human_support=needs_human_support,
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    @staticmethod
    def get_user_messages(db: Session, user_id: str):
        return (
            db.query(Message)
            .filter(Message.user_id == user_id)
            .order_by(Message.created_at.desc())
            .all()
        )
