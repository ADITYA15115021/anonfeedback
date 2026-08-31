from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router
from app.routes.feedback_page import router as feedback_page_router
from app.routes.feedback import router as feedback_router


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(auth_router)
app.include_router(feedback_page_router)
app.include_router(feedback_router)
