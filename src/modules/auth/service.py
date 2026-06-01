from sqlalchemy.orm import Session

from src.core.config import get_settings
from src.core.security import create_access_token, verify_password
from src.modules.auth.schemas import LoginRequest, RegisterRequest
from src.modules.users.models import User
from src.modules.users.schemas import UserCreate
from src.modules.users.service import UserService
from src.shared.errors import UnauthorizedError


class AuthService:
    def __init__(self, db: Session):
        self.user_service = UserService(db)

    def register(self, payload: RegisterRequest) -> User:
        return self.user_service.create_user(UserCreate(**payload.model_dump()))

    def login(self, payload: LoginRequest) -> dict:
        user = self.user_service.repository.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.password):
            raise UnauthorizedError("Invalid email or password")

        settings = get_settings()
        token = create_access_token(
            subject=str(user.id),
            claims={"email": user.email, "role": user.role},
        )
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in_minutes": settings.access_token_expire_minutes,
            "user": user,
        }
