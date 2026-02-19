from fastapi import APIRouter, HTTPException
from app.models import CreateUserRequest, User
from app.main import store

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=User, status_code=201)
def create_user(req: CreateUserRequest):
    try:
        return store.create_user(req.username)
    except ValueError:
        raise HTTPException(status_code=409, detail="username already exists")


@router.get("", response_model=list[User])
def list_users():
    return store.list_users()


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    user = store.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user