from pydantic import BaseModel, Field


class UserBase(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    segment: str | None = None

    class Config:
        from_attributes = True
