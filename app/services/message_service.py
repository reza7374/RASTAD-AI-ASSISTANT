from sqlalchemy.orm import Session

from app.repositories.message_repository import MessageRepository
from app.repositories.user_repository import UserRepository
from app.schemas.message_schema import MessageResponse
from app.services.intent_service import detect_intent
from app.services.knowledge_service import knowledge_service
from app.services.llm_service import llm_service
from app.services.segment_service import detect_segment


class MessageService:
    """
    Main orchestration service for processing user messages.
    Handles intent detection, memory, RAG retrieval and response generation.
    """

    HISTORY_LIMIT = 5

    @staticmethod
    def handle_message(
        db: Session,
        user_id: str,
        name: str,
        message: str,
    ) -> MessageResponse:

        # -----------------------------
        # 1️⃣ Detect intent and segment
        # -----------------------------
        intent = detect_intent(message)
        user_segment = detect_segment(intent)

        # -----------------------------
        # 2️⃣ Find or create user
        # -----------------------------
        user = UserRepository.get_by_user_id(db=db, user_id=user_id)

        if not user:
            user = UserRepository.create_user(
                db=db,
                user_id=user_id,
                name=name,
                segment=user_segment,
            )
        else:
            UserRepository.update_last_seen(db=db, user=user)

        # -----------------------------
        # 3️⃣ Get conversation history
        # -----------------------------
        history_messages = MessageRepository.get_recent_messages(
            db=db,
            user_id=user_id,
            limit=MessageService.HISTORY_LIMIT,
        )

        formatted_history = ""

        # reverse so oldest → newest
        for msg in reversed(history_messages):
            formatted_history += f"User: {msg.user_message}\n"
            formatted_history += f"Assistant: {msg.assistant_reply}\n"

        # -----------------------------
        # 4️⃣ Retrieve knowledge context
        # -----------------------------
        context = knowledge_service.build_context(
            query=message,
            top_k=2,
        )

        # -----------------------------
        # 5️⃣ Generate reply
        # -----------------------------
        reply = llm_service.generate_reply(
            user_message=message,
            context=context,
            intent=intent,
            user_segment=user_segment,
            history=formatted_history,
        )

        # -----------------------------
        # 6️⃣ Determine support escalation
        # -----------------------------
        needs_human_support = intent == "support_request"

        # -----------------------------
        # 7️⃣ Save conversation
        # -----------------------------
        MessageRepository.create_message(
            db=db,
            user_id=user_id,
            user_message=message,
            assistant_reply=reply,
            intent=intent,
            needs_human_support=needs_human_support,
        )

        # -----------------------------
        # 8️⃣ Return API response
        # -----------------------------
        return MessageResponse(
            reply=reply,
            intent=intent,
            user_segment=user_segment,
            needs_human_support=needs_human_support,
        )


message_service = MessageService()
