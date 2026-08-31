from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    message: str


class FeedbackResponse(BaseModel):
    id: int
    message: str

    class Config:
        from_attributes = True

        