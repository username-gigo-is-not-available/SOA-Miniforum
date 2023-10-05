from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str = Field(...)
    content: str = Field(...)


class PostCreate(PostBase):
    user_id: int = Field(...)


class PostUpdate(PostBase):
    pass
