from pydantic import BaseModel, Field


class MessageRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=100, description="Unique user identifier")
    name: str = Field(..., min_length=1, max_length=100, description="User display name")
    message: str = Field(..., min_length=1, max_length=2000, description="User message text")


class MessageResponse(BaseModel):
    reply: str
    intent: str
    user_segment: str
    needs_human_support: bool
