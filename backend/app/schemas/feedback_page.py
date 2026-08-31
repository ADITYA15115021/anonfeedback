from datetime import datetime

from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship

class FeedbackPageCreate(BaseModel):
    title: str
    description: str | None = None


class FeedbackPageResponse(BaseModel):
    id: int
    title: str
    description: str | None
    url: str
    accepting_feedback: bool
    created_at: datetime

    class Config:
        from_attributes = True


class FeedbackStatusUpdate(BaseModel):
    accepting_feedback: bool
