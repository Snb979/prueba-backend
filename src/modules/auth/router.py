from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.modules.auth.schemas import LoginRequest, RegisterRequest
from src.modules.auth.service import AuthService
from src.modules.users.schemas import UserRead
from src.shared.auth import get_current_user
from src.shared.responses import ok

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user = AuthService(db).register(payload)
    return ok("User registered successfully", UserRead.model_validate(user).model_dump(mode="json"), status=201)


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    token_data = AuthService(db).login(payload)
    token_data["user"] = UserRead.model_validate(token_data["user"]).model_dump(mode="json")
    return ok("Login successful", token_data)


@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return ok("Current user", UserRead.model_validate(current_user).model_dump(mode="json"))
