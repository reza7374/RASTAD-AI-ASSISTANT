from pydantic import BaseModel, Field


class MessageRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=100)
    message: str = Field(..., min_length=1, max_length=2000)


class MessageResponse(BaseModel):
    reply: str
    intent: str
    user_segment: str
    needs_human_support: bool
