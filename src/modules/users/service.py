from sqlalchemy.orm import Session

from src.core.security import hash_password
from src.modules.users.models import User
from src.modules.users.repository import UserRepository
from src.modules.users.schemas import UserCreate, UserUpdate
from src.shared.errors import ConflictError, NotFoundError


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return self.repository.list(skip=skip, limit=limit)

    def get_user(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    def create_user(self, payload: UserCreate) -> User:
        if self.repository.get_by_email(payload.email):
            raise ConflictError("Email is already registered")
        user = User(
            username=payload.username,
            email=payload.email,
            password=hash_password(payload.password),
            role=payload.role.value,
        )
        return self.repository.create(user)

    def update_user(self, user_id: int, payload: UserUpdate) -> User:
        user = self.get_user(user_id)
        if payload.email and payload.email != user.email:
            existing = self.repository.get_by_email(payload.email)
            if existing and existing.id != user_id:
                raise ConflictError("Email is already registered")
            user.email = payload.email
        if payload.username is not None:
            user.username = payload.username
        if payload.password is not None:
            user.password = hash_password(payload.password)
        if payload.role is not None:
            user.role = payload.role.value
        return self.repository.update(user)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        self.repository.delete(user)
