from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.modules.users.schemas import UserCreate, UserRead, UserUpdate
from src.modules.users.service import UserService
from src.shared.auth import require_admin
from src.shared.responses import ok

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")
def list_users(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    users = UserService(db).list_users(skip=skip, limit=limit)
    data = [UserRead.model_validate(user).model_dump(mode="json") for user in users]
    return ok("Users retrieved successfully", data, meta={"skip": skip, "limit": limit})


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    user = UserService(db).get_user(user_id)
    return ok("User retrieved successfully", UserRead.model_validate(user).model_dump(mode="json"))


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    user = UserService(db).create_user(payload)
    return ok("User created successfully", UserRead.model_validate(user).model_dump(mode="json"), status=201)


@router.put("/{user_id}")
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db), _=Depends(require_admin)):
    user = UserService(db).update_user(user_id, payload)
    return ok("User updated successfully", UserRead.model_validate(user).model_dump(mode="json"))


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    UserService(db).delete_user(user_id)
    return ok("User deleted successfully")
