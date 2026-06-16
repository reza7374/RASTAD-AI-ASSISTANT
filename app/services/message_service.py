from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.repositories.message_repository import MessageRepository
from app.services.intent_service import detect_intent


def handle_message(db: Session, user_id: str, name: str, message: str):

    user_repo = UserRepository(db)
    message_repo = MessageRepository(db)

    user = user_repo.get_by_user_id(user_id)

    if not user:
        user = user_repo.create_user(user_id=user_id, name=name)

    intent = detect_intent(message)

    reply = generate_mock_reply(intent)

    message_repo.create_message(
        user_id=user_id,
        user_message=message,
        assistant_reply=reply,
        intent=intent,
        needs_human_support=False
    )

    return {
        "reply": reply,
        "intent": intent,
        "user_segment": user.segment,
        "needs_human_support": False
    }


def generate_mock_reply(intent: str):

    replies = {
        "vip_question": "خدمات VIP راستاد شامل سیگنال‌های اختصاصی و تحلیل بازار است.",
        "exchange_registration": "برای ثبت نام در صرافی از لینک معرفی راستاد استفاده کنید.",
        "kol_collaboration": "برای همکاری به عنوان KOL اطلاعات شبکه اجتماعی خود را ارسال کنید.",
        "support_request": "درخواست شما به تیم پشتیبانی منتقل شد.",
        "general_info": "لطفا سوال خود را دقیق‌تر بپرسید."
    }

    return replies.get(intent, "متوجه سوال شما نشدم.")
