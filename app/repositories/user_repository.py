from sqlalchemy.orm import Session
from datetime import datetime

from app.db.models import User


class UserRepository:

    @staticmethod
    def get_by_user_id(db: Session, user_id: str):
        return db.query(User).filter(User.user_id == user_id).first()

    @staticmethod
    def create_user(db: Session, user_id: str, name: str, segment: str = "new_user"):
        user = User(
            user_id=user_id,
            name=name,
            segment=segment,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_last_seen(db: Session, user: User):
        user.last_seen_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100):

        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update_last_seen(db: Session, user_id: str):

        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            user.last_seen_at = datetime.utcnow()
            db.commit()
            db.refresh(user)
        return user
