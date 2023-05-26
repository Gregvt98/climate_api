from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .session import Base
from sqlalchemy.dialects.postgresql import JSONB


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    version = Column(String)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="posts")
    sentiment_analysis = relationship("SentimentAnalysis", back_populates="post", cascade="all, delete-orphan", uselist=False)
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")

class SentimentAnalysis(Base):
    __tablename__ = "sentiment_analysis"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    score = Column(Float)
    ratio = Column(Float)
    post_id = Column(Integer, ForeignKey("posts.id"), unique=True)
    post = relationship("Post", back_populates="sentiment_analysis")

class EventLog(Base):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, index=True)
    log_level = Column(String)
    ip_address = Column(String)
    user_agent = Column(String)
    event_type = Column(String)
    event_data = Column(JSONB)
    user_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)