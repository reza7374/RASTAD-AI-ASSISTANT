def detect_intent(message: str) -> str:
    text = message.lower()

    if "vip" in text:
        return "vip_question"

    if "صرافی" in text or "ثبت نام" in text:
        return "exchange_registration"

    if "kol" in text or "همکاری" in text:
        return "kol_collaboration"

    if "پشتیبانی" in text or "مشکل" in text:
        return "support_request"

    return "general_info"
