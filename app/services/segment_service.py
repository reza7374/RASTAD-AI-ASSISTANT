def detect_segment(intent: str) -> str:

    mapping = {
        "vip_question": "vip_interest",
        "exchange_registration": "exchange_signup",
        "kol_collaboration": "kol_candidate",
        "support_request": "support_needed",
        "general_info": "general_question"
    }

    return mapping.get(intent, "general_question")
