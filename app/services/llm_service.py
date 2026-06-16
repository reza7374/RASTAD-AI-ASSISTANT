class LLMService:
    """
    Service responsible for generating assistant replies.

    Current version:
    - mock / rule-based response generation
    Future version:
    - can be replaced by a real LLM provider
    """

    def generate_reply(
        self,
        user_message: str,
        context: str,
        intent: str,
        user_segment: str,
    ) -> str:
        """
        Generate a reply based on:
        - user message
        - retrieved knowledge context
        - detected intent
        - user segment
        """

        if context:
            return (
                f"بر اساس اطلاعات موجود:\n\n"
                f"{context}\n\n"
                f"اگر بخواهید، می‌توانم خلاصه‌تر یا دقیق‌تر هم توضیح دهم."
            )

        if intent == "support_request":
            return (
                "متوجه شدم که به پشتیبانی نیاز دارید. "
                "لطفاً مشکل خود را با جزئیات بیشتری توضیح دهید تا بهتر راهنمایی‌تان کنم."
            )

        if intent == "vip_question":
            return (
                "خدمات VIP راستاد برای کاربرانی مناسب است که به دنبال خدمات ویژه و پشتیبانی اختصاصی هستند. "
                "اگر مایل باشید، می‌توانم جزئیات بیشتری ارائه دهم."
            )

        if intent == "exchange_registration":
            return (
                "برای ثبت‌نام در صرافی، می‌توانم مراحل و نکات مهم را برای شما توضیح دهم."
            )

        if intent == "kol_collaboration":
            return (
                "برای همکاری در برنامه KOL، می‌توانم شرایط و روند همکاری را توضیح بدهم."
            )

        return (
            "ممنون از پیام شما. اگر درباره خدمات راستاد، VIP، ثبت‌نام صرافی یا همکاری سوالی دارید، خوشحال می‌شوم کمک کنم."
        )


llm_service = LLMService()
