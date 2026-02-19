from typing import Dict, List
from app.models import User, Note


class InMemoryStore:
    def __init__(self) -> None:
        self._next_user_id = 1
        self._next_note_id = 1
        self.users_by_id: Dict[int, User] = {}
        self.user_id_by_username: Dict[str, int] = {}
        self.notes_by_user_id: Dict[int, List[Note]] = {}

    def create_user(self, username: str) -> User:
        key = username.strip().lower()
        if key in self.user_id_by_username:
            raise ValueError("USERNAME_EXISTS")

        user = User(id=self._next_user_id, username=username.strip())
        self._next_user_id += 1

        self.users_by_id[user.id] = user
        self.user_id_by_username[key] = user.id
        self.notes_by_user_id[user.id] = []
        return user

    def get_user(self, user_id: int) -> User | None:
        return self.users_by_id.get(user_id)

    def list_users(self) -> List[User]:
        return sorted(self.users_by_id.values(), key=lambda u: u.id)

    def add_note(self, user_id: int, text: str, source: str | None = None) -> Note:
        if user_id not in self.users_by_id:
            raise KeyError("USER_NOT_FOUND")

        note = Note(
            id=self._next_note_id,
            user_id=user_id,
            text=text,
            source=source
        )
        self._next_note_id += 1

        self.notes_by_user_id[user_id].append(note)
        return note

    def list_notes(self, user_id: int) -> List[Note]:
        if user_id not in self.users_by_id:
            raise KeyError("USER_NOT_FOUND")
        return self.notes_by_user_id[user_id]