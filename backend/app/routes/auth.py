from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import engine
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.utils.security import (
    create_access_token,
    hash_password,
    verify_password,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post( "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate):

    with Session(engine) as session:

        statement = select(User).where(User.email == user_data.email)

        existing_user = session.scalars(statement).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        statement = select(User).where(
            User.username == user_data.username
        )

        existing_username = session.scalars(statement).first()

        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        hashed_password = hash_password(user_data.password)

        user = User(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        return user


@router.post("/login")
def login(user_data: UserLogin):

    with Session(engine) as session:

        statement = select(User).where(
            User.email == user_data.email
        )

        user = session.scalars(statement).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not verify_password(
            user_data.password,
            user.password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        access_token = create_access_token(
            {"sub": str(user.id)}
        )

        return {"access_token": access_token, "token_type": "bearer", "username": user.username}
