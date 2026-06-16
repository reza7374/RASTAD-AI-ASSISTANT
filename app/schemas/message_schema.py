from pydantic import BaseModel, Field
from datetime import datetime

class MessageRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=100, description="Unique user identifier")
    name: str = Field(..., min_length=1, max_length=100, description="User display name")
    message: str = Field(..., min_length=1, max_length=2000, description="User message text")




class MessageReplyResponse(BaseModel):
    reply: str
    intent: str
    user_segment: str
    needs_human_support: bool


class MessageRecordResponse(BaseModel):
    id: int
    user_id: str
    user_message: str
    assistant_reply: str
    intent: str
    needs_human_support: bool
    created_at: datetime

    class Config:
        from_attributes = True
