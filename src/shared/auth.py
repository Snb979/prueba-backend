from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.core.security import decode_access_token
from src.db.session import get_db
from src.modules.users.models import User
from src.modules.users.repository import UserRepository
from src.shared.errors import ForbiddenError, UnauthorizedError

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise UnauthorizedError()

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload.get("sub"))
    except (TypeError, ValueError):
        raise UnauthorizedError("Invalid or expired token")

    user = UserRepository(db).get_by_id(user_id)
    if not user:
        raise UnauthorizedError("User no longer exists")

    request.state.user_id = user.id
    request.state.user_role = user.role
    return user


def require_roles(*roles: str):
    allowed_roles = {role.lower() for role in roles}

    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role.lower() not in allowed_roles:
            raise ForbiddenError()
        return current_user

    return dependency


def require_admin(current_user: User = Depends(require_roles("admin"))) -> User:
    return current_user
