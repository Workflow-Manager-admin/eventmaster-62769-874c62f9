from typing import List, Optional
from datetime import datetime
from .models import (
    UserCreate,
    UserUpdate,
    UserResponse,
    EventCreate,
    EventUpdate,
    EventResponse,
    EventQuery
)



class InMemoryDB:
    """A minimal in-memory storage for demonstration. Not suitable for production."""

    def __init__(self):
        self.users = {}  # id: userdict
        self.events = {}  # id: eventdict
        self.user_id_counter = 1
        self.event_id_counter = 1

    # PUBLIC_INTERFACE
    def create_user(self, user: UserCreate) -> UserResponse:
        now = datetime.utcnow()
        user_dict = {
            'id': self.user_id_counter,
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'created_at': now,
        }
        self.users[self.user_id_counter] = user_dict
        resp = UserResponse(
            id=self.user_id_counter,
            username=user.username,
            email=user.email,
            created_at=now,
        )
        self.user_id_counter += 1
        return resp

    # PUBLIC_INTERFACE
    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[UserResponse]:
        udict = self.users.get(user_id)
        if not udict:
            return None
        if user_update.username is not None:
            udict['username'] = user_update.username
        if user_update.email is not None:
            udict['email'] = user_update.email
        if user_update.password is not None:
            udict['password'] = user_update.password
        return UserResponse(
            id=user_id,
            username=udict['username'],
            email=udict['email'],
            created_at=udict['created_at'],
        )

    # PUBLIC_INTERFACE
    def get_user(self, user_id: int) -> Optional[UserResponse]:
        udict = self.users.get(user_id)
        if not udict:
            return None
        return UserResponse(
            id=user_id,
            username=udict['username'],
            email=udict['email'],
            created_at=udict['created_at'],
        )

    # PUBLIC_INTERFACE
    def list_users(self) -> List[UserResponse]:
        return [
            UserResponse(
                id=u['id'],
                username=u['username'],
                email=u['email'],
                created_at=u['created_at'],
            )
            for u in self.users.values()
        ]

    # PUBLIC_INTERFACE
    def delete_user(self, user_id: int) -> bool:
        if user_id in self.users:
            # Delete all events by this user
            to_delete = [
                eid
                for eid, edict in self.events.items()
                if edict['creator_id'] == user_id
            ]
            for eid in to_delete:
                del self.events[eid]
            del self.users[user_id]
            return True
        return False

    # PUBLIC_INTERFACE
    def create_event(self, event: EventCreate, creator_id: int) -> Optional[EventResponse]:
        if creator_id not in self.users:
            return None
        now = datetime.utcnow()
        edict = {
            'id': self.event_id_counter,
            'title': event.title,
            'description': event.description,
            'location': event.location,
            'start_time': event.start_time,
            'end_time': event.end_time,
            'creator_id': creator_id,
            'created_at': now,
        }
        self.events[self.event_id_counter] = edict
        resp = EventResponse(**edict)
        self.event_id_counter += 1
        return resp

    # PUBLIC_INTERFACE
    def update_event(self, event_id: int, event_update: EventUpdate) -> Optional[EventResponse]:
        edict = self.events.get(event_id)
        if not edict:
            return None
        for f in ['title', 'description', 'location', 'start_time', 'end_time']:
            val = getattr(event_update, f)
            if val is not None:
                edict[f] = val
        return EventResponse(**edict)

    # PUBLIC_INTERFACE
    def get_event(self, event_id: int) -> Optional[EventResponse]:
        edict = self.events.get(event_id)
        if not edict:
            return None
        return EventResponse(**edict)

    # PUBLIC_INTERFACE
    def list_events(self, query: Optional[EventQuery] = None) -> List[EventResponse]:
        results = list(self.events.values())
        if query:
            if query.title:
                results = [
                    ev for ev in results
                    if query.title.strip().lower() in (ev['title'] or '').lower()
                ]
            if query.location:
                results = [
                    ev for ev in results
                    if query.location.strip().lower() in (ev['location'] or '').lower()
                ]
            if query.date_from:
                results = [ev for ev in results if ev['start_time'] >= query.date_from]
            if query.date_to:
                results = [ev for ev in results if ev['end_time'] <= query.date_to]
            if query.created_by:
                results = [
                    ev for ev in results if ev['creator_id'] == query.created_by
                ]
        return [EventResponse(**ev) for ev in results]

    # PUBLIC_INTERFACE
    def delete_event(self, event_id: int) -> bool:
        if event_id in self.events:
            del self.events[event_id]
            return True
        return False

db = InMemoryDB()


