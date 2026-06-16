from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.repositories.message_repository import MessageRepository
from app.services.intent_service import detect_intent
from app.services.segment_service import detect_segment


def handle_message(
    db: Session,
    user_id: str,
    name: str,
    message: str
):
    """
    Main pipeline for processing user messages.
    """

    if not user_id:
        raise ValueError("user_id is required")

    if not message or message.strip() == "":
        raise ValueError("message cannot be empty")

    user_repo = UserRepository(db)
    message_repo = MessageRepository(db)

    # ---------- get or create user ----------
    user = user_repo.get_by_user_id(user_id)

    # ---------- detect intent ----------
    intent = detect_intent(message)

    # ---------- detect user segment ----------
    segment = detect_segment(intent)

    if not user:
        user = user_repo.create_user(
            user_id=user_id,
            name=name,
            segment=segment
        )
    else:
        user_repo.update_last_seen(user)

    # ---------- determine if human support needed ----------
    needs_human_support = intent == "support_request"

    # ---------- generate reply ----------
    reply = generate_mock_reply(intent)

    # ---------- store message ----------
    message_repo.create_message(
        user_id=user_id,
        user_message=message,
        assistant_reply=reply,
        intent=intent,
        needs_human_support=needs_human_support
    )

    # ---------- response ----------
    return {
        "reply": reply,
        "intent": intent,
        "user_segment": segment,
        "needs_human_support": needs_human_support
    }


def generate_mock_reply(intent: str) -> str:
    """
    Temporary mock responses instead of real LLM.
    """

    replies = {
        "vip_question": (
            "خدمات VIP راستاد شامل سیگنال‌های اختصاصی، تحلیل حرفه‌ای بازار "
            "و دسترسی به فرصت‌های ویژه سرمایه‌گذاری است."
        ),

        "exchange_registration": (
            "برای ثبت‌نام در صرافی می‌توانید از لینک معرفی راستاد استفاده کنید. "
            "پس از ثبت‌نام و احراز هویت، امکان استفاده از خدمات فراهم می‌شود."
        ),

        "kol_collaboration": (
            "برای همکاری به عنوان KOL با راستاد لطفاً اطلاعات شبکه اجتماعی "
            "و میزان فالوور خود را ارسال کنید تا تیم همکاری با شما تماس بگیرد."
        ),

        "support_request": (
            "درخواست شما ثبت شد و تیم پشتیبانی راستاد در اسرع وقت با شما "
            "ارتباط خواهد گرفت."
        ),

        "general_info": (
            "برای اطلاعات بیشتر درباره خدمات راستاد می‌توانید سوال خود را "
            "کمی دقیق‌تر مطرح کنید."
        )
    }

    return replies.get(
        intent,
        "متوجه سوال شما نشدم. لطفاً سوال خود را واضح‌تر بپرسید."
    )
    