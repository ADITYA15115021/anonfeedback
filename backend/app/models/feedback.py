from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)

    feedback_page_id = Column(
        Integer,
        ForeignKey("feedback_pages.id"),
        nullable=False
    )

    message = Column(String, nullable=False)

    feedback_page = relationship(
        "FeedbackPage",
        back_populates="feedbacks"
    )