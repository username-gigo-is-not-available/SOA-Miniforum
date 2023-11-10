import datetime

from pydantic import BaseModel, Field


class NotificationBase(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    timestamp: datetime = Field(...)


class NotificationCreate(NotificationBase):
    user_id: int = Field(...)


class NotificationUpdate(NotificationBase):
    pass
