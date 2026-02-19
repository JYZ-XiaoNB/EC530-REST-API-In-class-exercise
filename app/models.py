from pydantic import BaseModel, Field
from typing import Optional


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=1, max_length=50)


class User(BaseModel):
    id: int
    username: str


class CreateNoteRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    source: Optional[str] = None


class Note(BaseModel):
    id: int
    user_id: int
    text: str
    source: Optional[str] = None