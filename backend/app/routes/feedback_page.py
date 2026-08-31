from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import engine
from app.models.feedback_page import FeedbackPage
from app.models.user import User
from app.schemas.feedback_page import (
    FeedbackPageCreate,
    FeedbackPageResponse,
    FeedbackStatusUpdate
)
from app.utils.security import get_current_user


router = APIRouter(
    prefix="/feedback-pages",
    tags=["Feedback Pages"]
)


@router.post( "",response_model=FeedbackPageResponse,status_code=status.HTTP_201_CREATED)
def create_feedback_page(
    page_data: FeedbackPageCreate,
    current_user: User = Depends(get_current_user),
):
    with Session(engine) as session:
        page = FeedbackPage(
            user_id=current_user.id,
            title=page_data.title,
            description=page_data.description
        )

        session.add(page)
        session.commit()
        session.refresh(page)

        return {
            "id": page.id,
            "title": page.title,
            "description": page.description,
            "url": f"/feedback/{current_user.username}/{page.id}",
            "accepting_feedback": page.accepting_feedback,
            "created_at": page.created_at,
        }


@router.patch("/{page_id}/status")
def update_feedback_status(
    page_id: int,
    status_data: FeedbackStatusUpdate,
    current_user: User = Depends(get_current_user)
):
    with Session(engine) as session:
        statement = select(FeedbackPage).where(
            FeedbackPage.id == page_id,
            FeedbackPage.user_id == current_user.id
        )

        page = session.scalars(statement).first()

        if not page:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feedback page not found"
            )

        page.accepting_feedback = status_data.accepting_feedback

        session.commit()
        session.refresh(page)

        return {
            "accepting_feedback": page.accepting_feedback
        }


@router.get("", response_model=list[FeedbackPageResponse])
def list_feedback_pages(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        pages = session.scalars(
            select(FeedbackPage)
            .where(FeedbackPage.user_id == current_user.id)
            .order_by(FeedbackPage.id.desc())
        ).all()
        return [{
            "id": page.id,
            "title": page.title,
            "description": page.description,
            "url": f"/feedback/{current_user.username}/{page.id}",
            "accepting_feedback": page.accepting_feedback,
            "created_at": page.created_at,
        } for page in pages]
