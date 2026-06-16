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
    """

    @staticmethod
    def handle_message(
        db: Session,
        user_id: str,
        name: str,
        message: str,
    ) -> MessageResponse:
        """
        Process incoming user message through the full pipeline:

        1. Find or create user
        2. Update user activity
        3. Detect intent
        4. Detect user segment
        5. Retrieve relevant knowledge
        6. Generate assistant reply
        7. Determine if human support is needed
        8. Save message in database
        9. Return structured API response
        """

        # 1. Find existing user or create a new one
        user = UserRepository.get_by_user_id(db=db, user_id=user_id)

        # 2. Detect intent first
        intent = detect_intent(message)

        # 3. Detect user segment
        user_segment = detect_segment(intent)

        if not user:
            user = UserRepository.create_user(
                db=db,
                user_id=user_id,
                name=name,
                segment=user_segment,
            )
        else:
            # optional: update name if changed
            UserRepository.update_last_seen(db=db, user=user)

        # 4. Retrieve relevant knowledge context
        context = knowledge_service.build_context(query=message, top_k=3)

        # 5. Generate assistant reply
        reply = llm_service.generate_reply(
            user_message=message,
            context=context,
            intent=intent,
            user_segment=user_segment,
        )

        # 6. Decide whether human support is needed
        needs_human_support = intent == "support_request"

        # 7. Save conversation in database
        MessageRepository.create_message(
            db=db,
            user_id=user_id,
            user_message=message,
            assistant_reply=reply,
            intent=intent,
            needs_human_support=needs_human_support,
        )

        # 8. Return API response
        return MessageResponse(
            reply=reply,
            intent=intent,
            user_segment=user_segment,
            needs_human_support=needs_human_support,
        )


message_service = MessageService()
