from pydantic import BaseModel


class MessageRequest(BaseModel):
    user_id: str
    name: str
    message: str


class MessageResponse(BaseModel):
    reply: str
    intent: str
    user_segment: str
    needs_human_support: bool
