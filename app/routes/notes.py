from fastapi import APIRouter, HTTPException
from app.models import CreateNoteRequest, Note
from app.main import store

router = APIRouter(prefix="/users/{user_id}/notes", tags=["notes"])


@router.post("", response_model=Note, status_code=201)
def add_note(user_id: int, req: CreateNoteRequest):
    try:
        return store.add_note(user_id=user_id, text=req.text, source=req.source)
    except KeyError:
        raise HTTPException(status_code=404, detail="user not found")


@router.get("", response_model=list[Note])
def list_notes(user_id: int):
    try:
        return store.list_notes(user_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="user not found")