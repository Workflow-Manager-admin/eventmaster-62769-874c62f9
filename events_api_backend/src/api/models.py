from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


# PUBLIC_INTERFACE


class EventCreateWithCreator(BaseModel):
    """Model for event creation, including creator_id at root level for OpenAPI safety."""
    event: "EventCreate" = Field(..., description="Event details (title, dates, etc.)")
    creator_id: int = Field(..., description="ID of the user creating the event")

# PUBLIC_INTERFACE

class UserBase(BaseModel):
    """Base model for a user."""
    username: str = Field(..., description="Unique username for the user")
    email: EmailStr = Field(..., description="User email address")


# PUBLIC_INTERFACE
class UserCreate(UserBase):
    """Model for creating a new user."""
    password: str = Field(
        ..., min_length=6, description="User password (min 6 characters)"
    )


# PUBLIC_INTERFACE
class UserUpdate(BaseModel):
    """Model for updating an existing user."""
    username: Optional[str] = Field(None, description="Updated username")
    email: Optional[EmailStr] = Field(None, description="Updated email address")
    password: Optional[str] = Field(
        None, min_length=6, description="Updated password (min 6 characters)"
    )


# PUBLIC_INTERFACE
class UserResponse(UserBase):
    """Response model for user data."""
    id: int = Field(..., description="User identifier")
    created_at: datetime = Field(..., description="User creation timestamp")

    class Config:
        orm_mode = True


# PUBLIC_INTERFACE
class EventBase(BaseModel):
    """Base model for an event."""
    title: str = Field(..., description="Title of the event")
    description: Optional[str] = Field(None, description="Description of the event")
    location: Optional[str] = Field(None, description="Event location")
    start_time: datetime = Field(..., description="Event start date and time")
    end_time: datetime = Field(..., description="Event end date and time")


# PUBLIC_INTERFACE
class EventCreate(EventBase):
    """Model for creating a new event."""
    pass


# PUBLIC_INTERFACE
class EventUpdate(BaseModel):
    """Model for updating an existing event."""
    title: Optional[str] = Field(None, description="Updated event title")
    description: Optional[str] = Field(None, description="Updated description")
    location: Optional[str] = Field(None, description="Updated location")
    start_time: Optional[datetime] = Field(None, description="Updated start date/time")
    end_time: Optional[datetime] = Field(None, description="Updated end date/time")


# PUBLIC_INTERFACE
class EventResponse(EventBase):
    """Response model for event data."""
    id: int = Field(..., description="Event identifier")
    creator_id: int = Field(..., description="ID of the creating user")
    created_at: datetime = Field(..., description="Event creation timestamp")

    class Config:
        orm_mode = True


# PUBLIC_INTERFACE
class EventQuery(BaseModel):
    """Model for querying events."""
    title: Optional[str] = Field(
        None, description="Filter by event title (substring match)"
    )
    date_from: Optional[datetime] = Field(
        None, description="Events starting after this date/time"
    )
    date_to: Optional[datetime] = Field(
        None, description="Events ending before this date/time"
    )
    location: Optional[str] = Field(
        None, description="Filter by event location (substring match)"
    )
    created_by: Optional[int] = Field(
        None, description="Filter events created by user ID"
    )


# PUBLIC_INTERFACE
class Message(BaseModel):
    """Basic message model for API responses."""
    message: str
