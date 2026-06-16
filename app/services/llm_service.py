class LLMService:
    """
    Service responsible for generating assistant replies.

    Current version:
    - rule-based mock responses
    - supports conversation history and retrieved context

    Future version:
    - replace with real LLM (OpenAI / Ollama / HF)
    """

    def generate_reply(
        self,
        user_message: str,
        context: str,
        intent: str,
        user_segment: str,
        history: str = "",
    ) -> str:
        """
        Generate assistant reply based on:
        - conversation history
        - retrieved knowledge context
        - detected intent
        - user segment
        """

        # -----------------------------
        # 1️⃣ Knowledge-based response
        # -----------------------------
        if context:
            return (
                "بر اساس اطلاعات موجود:\n\n"
                f"{context}\n\n"
                "اگر بخش خاصی از این اطلاعات برای شما مهم است "
                "می‌توانم آن را ساده‌تر یا دقیق‌تر توضیح دهم."
            )

        # -----------------------------
        # 2️⃣ Intent-based responses
        # -----------------------------
        if intent == "support_request":
            return (
                "به نظر می‌رسد به پشتیبانی نیاز دارید. "
                "لطفاً مشکل خود را با جزئیات بیشتری توضیح دهید تا بتوانم بهتر راهنمایی‌تان کنم."
            )

        if intent == "vip_question":
            return (
                "خدمات VIP راستاد برای کاربرانی طراحی شده که به دنبال خدمات حرفه‌ای‌تر "
                "و پشتیبانی اختصاصی هستند.\n\n"
                "اگر مایل باشید می‌توانم درباره مزایا، شرایط و نحوه دریافت این خدمات "
                "بیشتر توضیح بدهم."
            )

        if intent == "exchange_registration":
            return (
                "برای ثبت‌نام در صرافی می‌توانم مراحل کامل ثبت‌نام و نکات مهم امنیتی "
                "را برای شما توضیح بدهم.\n\n"
                "اگر صرافی خاصی مدنظر دارید هم بفرمایید تا دقیق‌تر راهنمایی کنم."
            )

        if intent == "kol_collaboration":
            return (
                "برنامه همکاری KOL برای افرادی طراحی شده که جامعه کاربری فعال دارند "
                "و می‌خواهند با راستاد همکاری کنند.\n\n"
                "اگر دوست داشته باشید می‌توانم شرایط همکاری و مراحل شروع را توضیح بدهم."
            )

        # -----------------------------
        # 3️⃣ Fallback response
        # -----------------------------
        return (
            "ممنون از پیام شما.\n\n"
            "اگر درباره خدمات راستاد، برنامه VIP، ثبت‌نام صرافی "
            "یا همکاری KOL سوالی دارید خوشحال می‌شوم کمک کنم."
        )


llm_service = LLMService()
