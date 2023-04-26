#copy of users.py

from fastapi import APIRouter, Request, Depends, Response, encoders, BackgroundTasks
import typing as t
import requests

from app.db.session import get_db
from app.db.crud import (
    edit_post,
    get_post,
    create_sentiment_analysis
)
from app.db.schemas import PostEdit, SentimentAnalysisBase, SentimentAnalysisOut
from app.core.auth import get_current_active_user, get_current_active_superuser

analysis_router = r = APIRouter()

@r.get("/analysis/test")
async def root():
    return {"message": "Hello from analysis"}

@r.post("/analyze/{post_id}", response_model=SentimentAnalysisOut, response_model_exclude_none=True)
async def sentiment_analysis_create(
    post_id: int,
    db=Depends(get_db)
):
    """
    Create a new sentiment analysis
    """
    return create_sentiment_analysis(db, post_id)


