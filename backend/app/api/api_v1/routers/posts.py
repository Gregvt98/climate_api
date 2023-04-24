#copy of users.py

from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t

from app.db.session import get_db
from app.db.crud import (
    get_posts,
    get_user_posts,
    get_post,
    create_post,
    delete_post,
    edit_post,
)
from app.db.schemas import PostCreate, PostEdit, Post, PostOut
from app.core.auth import get_current_active_user, get_current_active_superuser

posts_router = r = APIRouter()


@r.get(
    "/posts",
    response_model=t.List[Post],
    response_model_exclude_none=True,
)
async def posts_list(
    response: Response,
    db=Depends(get_db),
    #current_user=Depends(get_current_active_superuser),
):
    """
    Get all posts
    """
    posts = get_posts(db)
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
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Create a new post
    """
    return create_post(db, post, current_user.id)


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
