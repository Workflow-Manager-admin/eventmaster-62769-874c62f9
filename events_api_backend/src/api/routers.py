from fastapi import APIRouter, HTTPException, Path, Query, Body, status
from typing import List, Optional
from .models import (
    UserCreate,
    UserUpdate,
    UserResponse,
    EventCreate,
    EventUpdate,
    EventResponse,
    EventQuery,
    Message
)
from .database import db


router = APIRouter()


# USERS

@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with username, email, and password.",
    tags=["Users"],
)
# PUBLIC_INTERFACE
def create_user(user: UserCreate):
    existing_user = next(
        (
            u
            for u in db.users.values()
            if u['email'] == user.email or u['username'] == user.username
        ),
        None,
    )
    if existing_user:
        raise HTTPException(
            status_code=409, detail="User with this email or username already exists"
        )
    return db.create_user(user)


@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Get a user",
    description="Fetch details of a user by ID.",
    tags=["Users"],
)
# PUBLIC_INTERFACE
def get_user(user_id: int = Path(..., ge=1, description="User ID")):
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get(
    "/users",
    response_model=List[UserResponse],
    summary="List users",
    description="List all users.",
    tags=["Users"],
)
# PUBLIC_INTERFACE
def list_users():
    return db.list_users()


@router.put(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Update a user",
    description="Update an existing user's information.",
    tags=["Users"],
)
# PUBLIC_INTERFACE
def update_user(user_id: int, user: UserUpdate):
    result = db.update_user(user_id, user)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.delete(
    "/users/{user_id}",
    response_model=Message,
    summary="Delete a user",
    description="Delete a user and all their events.",
    tags=["Users"],
)
# PUBLIC_INTERFACE
def delete_user(user_id: int):
    success = db.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return Message(message="User deleted")


# EVENTS

@router.post(
    "/events",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new event",
    description="Create a new event. The `creator_id` must be a valid user.",
    tags=["Events"],
)
# PUBLIC_INTERFACE
def create_event(
    event: EventCreate,
    creator_id: int = Body(..., embed=True, description="ID of the user creating the event"),
):
    created_event = db.create_event(event, creator_id=creator_id)
    if not created_event:
        raise HTTPException(status_code=404, detail="Creator user not found")
    return created_event


@router.get(
    "/events/{event_id}",
    response_model=EventResponse,
    summary="Get an event",
    description="Fetch details of an event by ID.",
    tags=["Events"],
)
# PUBLIC_INTERFACE
def get_event(event_id: int = Path(..., ge=1, description="Event ID")):
    event = db.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.get(
    "/events",
    response_model=List[EventResponse],
    summary="List & query events",
    description="List all events or query by title, date range, location, or creator.",
    tags=["Events"],
)
# PUBLIC_INTERFACE
def list_events(
    title: Optional[str] = Query(None, description="Search for substring in event title"),
    date_from: Optional[str] = Query(
        None, description="Filter events starting from this ISO datetime"
    ),
    date_to: Optional[str] = Query(
        None, description="Filter events ending before this ISO datetime"
    ),
    location: Optional[str] = Query(None, description="Search for substring in location"),
    created_by: Optional[int] = Query(None, description="ID of the creator user"),
):
    query = EventQuery(
        title=title,
        location=location,
        created_by=created_by,
    )
    from datetime import datetime
    if date_from:
        try:
            query.date_from = datetime.fromisoformat(date_from)
        except Exception:
            raise HTTPException(
                status_code=400, detail="Invalid date_from format. Use ISO8601."
            )
    if date_to:
        try:
            query.date_to = datetime.fromisoformat(date_to)
        except Exception:
            raise HTTPException(
                status_code=400, detail="Invalid date_to format. Use ISO8601."
            )
    return db.list_events(query=query)


@router.put(
    "/events/{event_id}",
    response_model=EventResponse,
    summary="Update an event",
    description="Update an existing event by ID.",
    tags=["Events"],
)
# PUBLIC_INTERFACE
def update_event(event_id: int, event: EventUpdate):
    updated = db.update_event(event_id, event)
    if not updated:
        raise HTTPException(status_code=404, detail="Event not found")
    return updated


@router.delete(
    "/events/{event_id}",
    response_model=Message,
    summary="Delete an event",
    description="Delete an event by ID.",
    tags=["Events"],
)
# PUBLIC_INTERFACE
def delete_event(event_id: int):
    success = db.delete_event(event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")
    return Message(message="Event deleted")
