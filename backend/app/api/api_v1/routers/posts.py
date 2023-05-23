#copy of users.py

from fastapi import APIRouter, Request, Depends, Response, encoders, BackgroundTasks
import typing as t
from typing import Union

from app.db.session import get_db
from app.db.crud import (
    get_posts,
    get_user_posts,
    get_post,
    create_post,
    delete_post,
    edit_post,
    create_sentiment_analysis,
    create_comment
)
from app.db.schemas import PostCreate, PostEdit, Post, PostOut, CommentCreate
from app.core.auth import get_current_active_user, get_current_active_superuser

posts_router = r = APIRouter()


@r.get(
    "/posts",
    response_model=t.List[PostOut],
    response_model_exclude_none=True,
)
async def posts_list(
    response: Response,
    db=Depends(get_db),
    limit: Union[int, None] = 100,
    q: Union[str, None] = None,
    #current_user=Depends(get_current_active_superuser),
):
    """
    Get all posts

    Optional filter on sentiment positivity/negativity, and date created > to be added
    """
    if q is None or q == "":
        posts = get_posts(db, limit=limit)
    elif q == "positive" or q == "negative":
        posts = get_posts(db, limit=limit, q=q)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(posts)}"
    return posts


@r.get("/posts/me", response_model=Post, response_model_exclude_none=True)
async def post_me(db=Depends(get_db), current_user=Depends(get_current_active_user)):
    """
    Get own posts
    """
    posts = get_user_posts(db, current_user.id)
    return posts

@r.get(
    "/posts/{post_id}",
    response_model=Post,
    response_model_exclude_none=True,
)
async def post_details(
    request: Request,
    post_id: int,
    db=Depends(get_db),
    #current_user=Depends(get_current_active_user),
):
    """
    Get any post details
    """
    post = get_post(db, post_id)
    return post
    # return encoders.jsonable_encoder(
    #     user, skip_defaults=True, exclude_none=True,
    # )


@r.post("/posts", response_model=Post, response_model_exclude_none=True)
async def post_create(
    request: Request,
    post: PostCreate,
    background_tasks: BackgroundTasks,
    db=Depends(get_db),
    #current_user=Depends(get_current_active_user),
):
    """
    Create a new post
    """
    created_post = create_post(db, post)
    #background task to analyze sentiment after it's created
    background_tasks.add_task(create_sentiment_analysis, db, created_post.id)
    return created_post


@r.put(
    "/posts/{post_id}", response_model=Post, response_model_exclude_none=True
)
async def post_edit(
    request: Request,
    post_id: int,
    post: PostEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Update existing post
    """
    return edit_post(db, post_id, post)


@r.delete(
    "/posts/{post_id}", response_model=Post, response_model_exclude_none=True
)
async def post_delete(
    request: Request,
    post_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Delete existing post
    """
    return delete_post(db, post_id)

@r.post("/posts/{post_id}/comments")
async def post_comment(
    post_id: int, 
    comment: CommentCreate, 
    db=Depends(get_db)
    #current_user: User = Depends(get_current_user),
):
    """
    Create a comment
    """
    return create_comment(db, comment, post_id)
    