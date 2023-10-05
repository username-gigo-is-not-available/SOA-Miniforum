from bson import ObjectId
from pydantic import BaseModel, Field
from src.database_models import PyObjectId


class CommentBase(BaseModel):
    content: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class CommentCreate(CommentBase):
    user_id: int = Field(...)
    post_id: PyObjectId = Field(...)


class CommentUpdate(CommentBase):
    pass
