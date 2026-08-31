from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import engine
from app.models.user import User
from app.models.feedback_page import FeedbackPage
from app.models.feedback import Feedback
from app.schemas.feedback_page import FeedbackPageResponse
from app.schemas.feedback import (
    FeedbackCreate,
    FeedbackResponse,
)

from app.utils.security import get_current_user


router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"]
)


@router.get("/{username}/{page_id}", response_model=FeedbackPageResponse)
def get_feedback_page(username: str, page_id: int):

    with Session(engine) as session:
        statement = (select(User)
            .where(User.username == username)
        )

        user = session.scalars(statement).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        statement = select(FeedbackPage).where(FeedbackPage.id == page_id, FeedbackPage.user_id == user.id)

        page = session.scalars(statement).first()

        if not page:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail="Feedback page not found"
            )

        return {
            "id": page.id,
            "title": page.title,
            "description": page.description,
            "url": f"/feedback/{user.username}/{page.id}",
            "accepting_feedback": page.accepting_feedback,
            "created_at": page.created_at,
        }


@router.post("/{username}/{page_id}", status_code=status.HTTP_201_CREATED)
def submit_feedback(username: str, page_id: int, feedback_data: FeedbackCreate):

    with Session(engine) as session:

        statement = (
            select(User)
            .where(User.username == username)
        )

        user = session.scalars(statement).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        statement = select(FeedbackPage).where(FeedbackPage.id == page_id, FeedbackPage.user_id == user.id)

        page = session.scalars(statement).first()

        if not page:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feedback page not found"
            )

        if not page.accepting_feedback:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This user is not currently accepting feedback"
            )

        feedback = Feedback(
            feedback_page_id=page.id,
            message=feedback_data.message
        )

        session.add(feedback)
        session.commit()
        session.refresh(feedback)

        return feedback


@router.get("/pages/{page_id}/feedback", response_model=list[FeedbackResponse])
def get_feedback(page_id: int, current_user: User = Depends(get_current_user)):

    with Session(engine) as session:

        statement = (
            select(FeedbackPage)
            .where(
                FeedbackPage.id == page_id,
                FeedbackPage.user_id == current_user.id
            )
        )

        page = session.scalars(statement).first()

        if not page:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feedback page not found"
            )

        statement = (
            select(Feedback)
            .where(
                Feedback.feedback_page_id == page.id
            )
        )

        feedbacks = session.scalars(statement).all()

        return feedbacks
