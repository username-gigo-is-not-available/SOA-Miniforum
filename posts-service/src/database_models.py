from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Post(BaseModel):
    id: PyObjectId = Field(..., alias="_id")
    title: str = Field(...)
    content: str = Field(...)
    timestamp: datetime = Field(...)
    user_id: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "61234567890abcdef123456",
                "title": "Sample Title",
                "content": "Sample Content",
                "timestamp": "2022-01-01T12:00:00Z",
                "user_id": 123
            }
        }

