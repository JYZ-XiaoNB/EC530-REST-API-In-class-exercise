from fastapi import FastAPI
from app.storage import InMemoryStore

store = InMemoryStore()

app = FastAPI(title="REST API In-class Exercise")

from app.routes.users import router as users_router
from app.routes.notes import router as notes_router

app.include_router(users_router)
app.include_router(notes_router)