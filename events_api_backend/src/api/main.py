from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import router


app = FastAPI(
    title="EventMaster Events Management API",
    description="""
EventMaster is an API for managing events, supporting CRUD operations and advanced querying.

**Main features**
- User registration & management
- Event creation, update, deletion, and retrieval
- Query events by title, time, location, or creator
    """,
    version="1.0.0",
    contact={
        "name": "EventMaster Team",
        "email": "support@eventmaster.local",
    },
    openapi_tags=[
        {
            "name": "Users",
            "description": "Manage users (create, update, delete, list, retrieve).",
        },
        {"name": "Events", "description": "Manage and query events."},
    ],
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Meta"])
def health_check():
    """
    Health check endpoint.
    """
    return {"message": "Healthy"}


# PUBLIC_INTERFACE
app.include_router(router)
