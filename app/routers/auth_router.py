from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.oauth2 import get_current_user

from app.schemas.user import UserCreate

from app.services.auth_service import (
    register_user,
    login_user,
    get_logged_in_user
)

router = APIRouter()


# ===============================
# Register
# ===============================
@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return register_user(user, db)


# ===============================
# Login
# ===============================
@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return login_user(request, db)


# ===============================
# Current User
# ===============================
@router.get("/me")
def me(
    current_user=Depends(get_current_user)
):
    return get_logged_in_user(current_user)