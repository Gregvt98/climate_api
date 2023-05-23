#copy of users.py

from fastapi import APIRouter, Request, Depends, Response, encoders, BackgroundTasks
import typing as t
from typing import Union

from app.db.session import get_db
from app.db.crud import (
    get_event,
    create_event
)
from app.db.schemas import EventBase, EventCreate, EventEdit, EventOut
from app.core.auth import get_current_active_user, get_current_active_superuser

events_router = r = APIRouter()

@r.get(
    "/events",
    response_model=t.List[EventBase],
    response_model_exclude_none=True,
)
async def events_list(
    response: Response,
    db=Depends(get_db),
    #current_user=Depends(get_current_active_superuser),
):
    """
    Get all events

    """
    pass

@r.get(
    "/events/{event_id}",
    response_model=EventOut,
    response_model_exclude_none=True,
)
async def event_details(
    request: Request,
    event_id: int,
    db=Depends(get_db),
    #current_user=Depends(get_current_active_user),
):
    """
    Get any event details
    """
    event = get_event(db, event_id)
    return event


@r.post("/events", response_model=EventOut, response_model_exclude_none=True)
async def event_create(
    request: Request,
    event: EventCreate,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Create a new event
    """
    created_event = create_event(db, event, current_user.id)
    return created_event

@r.put(
    "/posts/{event_id}", response_model=EventBase, response_model_exclude_none=True
)
async def event_edit(
    request: Request,
    event_id: int,
    event: EventEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Update existing event
    """
    return edit_event(db, event_id, event)


@r.delete(
    "/events/{event_id}", response_model=EventBase, response_model_exclude_none=True
)
async def event_delete(
    request: Request,
    event_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Delete existing event
    """
    return delete_event(db, event_id)
