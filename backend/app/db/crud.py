from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t
import requests
import json

from . import models, schemas
from app.core.security import get_password_hash
from app.core.config import SA_API

def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(db: Session, email: str) -> schemas.UserHashedPassword:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.UserOut]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return user


def edit_user(
    db: Session, user_id: int, user: schemas.UserEdit
) -> schemas.User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#crud posts

def get_post(db: Session, post_id: int):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


def get_user_posts(db: Session, user_id: int):
    post = db.query(models.Post).filter(models.Post.user_id == user_id).all()
    if not post:
        raise HTTPException(status_code=404, detail="Users posts not found")
    return post


def get_posts(
    db: Session, skip: int = 0, limit: int = 100, q: str = None
) -> t.List[schemas.PostOut]:
    if q is None:
        return db.query(models.Post).join(models.SentimentAnalysis).offset(skip).limit(limit).all()
    elif q == "positive" or q == "negative":
        ### if q is not empty, filter posts on sentiment positivity/negativity
        return db.query(models.Post).join(models.SentimentAnalysis).filter(models.SentimentAnalysis.type == q).offset(skip).limit(limit).all()
    else:
        raise HTTPException(status_code=404, detail="q parameter must be none, positive, or negative")

def create_post(db: Session, post: schemas.PostCreate): #need to pass user id as well
    #db_user = get_user(db, user_id) #get user with id

    db_post = models.Post(
        title=post.title,
        content=post.content,
        user_id=post.user_id,
        longitude=post.longitude,
        latitude=post.latitude,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int):
    post = get_post(db, post_id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
    db.delete(post)
    db.commit()
    return post


def edit_post(
    db: Session, post_id: int, post: schemas.PostEdit
) -> schemas.Post:
    db_post = get_post(db, post_id)
    if not db_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
    update_data = post.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_post, key, value)

    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_sentiment(post_id, text):
    url = "https://twinword-sentiment-analysis.p.rapidapi.com/analyze/"
    querystring = {"text": text}
    headers = {
        "content-type": "application/octet-stream",
        "X-RapidAPI-Key": SA_API, #"e1aa69a1fdmsh97353a2245ac9ebp1f5715jsne703986c7ca6", #hide key (use config.SA_API) of sentiment analysis API, 9000 free requests per month
        "X-RapidAPI-Host": "twinword-sentiment-analysis.p.rapidapi.com",
    }
    response = requests.get(url, headers=headers, params=querystring)
    json_response = response.json()
    #print(response.json())
    return json_response

def create_sentiment_analysis(db: Session,  post_id: int):
    db_post = get_post(db, post_id)
    if db_post.title and db_post.content:
        res = get_sentiment(db_post.id, db_post.title + db_post.content)
    elif db_post.title:
        res = get_sentiment(db_post.id, db_post.title)
    elif db_post.content:
        res = get_sentiment(db_post.id, db_post.content)
    print("sentiment_analysis: ", res)
    db_sentiment_analysis = models.SentimentAnalysis(
        type=res["type"],
        score=res["score"],
        ratio=res["ratio"],
        post_id=db_post.id,
    )
    db.add(db_sentiment_analysis)
    db.commit()
    db.refresh(db_sentiment_analysis)
    return db_sentiment_analysis

def get_sentiment_analysis(db: Session, sentiment_id: int):
    sentiment = db.query(models.SentimentAnalysis).filter(models.SentimentAnalysis.id == sentiment_id).first()
    if not sentiment:
        raise HTTPException(status_code=404, detail="Sentiment not found")
    return sentiment

def get_sentiment_analysis_by_post(db: Session, post_id: int):
    sentiment = db.query(models.SentimentAnalysis).filter(models.SentimentAnalysis.post_id == post_id).first()
    if not sentiment:
        raise HTTPException(status_code=404, detail="Sentiment not found")
    return sentiment

def get_event(db: Session, event_id: int):
    event = db.query(models.EventLog).filter(models.EventLog.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

def create_event(db: Session, event: schemas.EventCreate, user_id: int):
    json_data = json.dumps(event.event_data)
    db_event = models.EventLog(
        log_level = event.log_level,
        ip_address = event.ip_address,
        user_agent = event.user_agent,
        event_type = event.event_type,
        event_data = json_data,
        user_id = user_id,
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def create_comment(db: Session, comment: schemas.CommentCreate, post_id: int):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db_comment = models.Comment(
        content=comment.content,
        post_id=post_id,
        user_id=comment.user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment