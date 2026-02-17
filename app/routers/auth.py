from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.crud import user as user_crud
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import verify_password, create_access_token, get_current_user, get_password_hash, get_current_active_superuser
from app.core.config import settings
from app.models.user import User
from datetime import timedelta

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post(
    "/register",
    response_model = UserResponse,
    status_code = status.HTTP_201_CREATED,
)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = user_crud.get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail = "Email ya registrado",
        )
    user = user_crud.create_user(db, user_in)
    return user

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = user_crud.get_user_by_email(db, email = form_data.username)

    if not user:
        raise HTTPException(
            status_code = 400,
            detail = "Correo o contraseña incorrectos",
        )
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code = 400,
            detail = "Correo o contraseña incorrectos",
        )
    
    access_token_expires = timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sub": str(user.id)},
        expires_delta = access_token_expires,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user=Depends(get_current_user)):
    return current_user


@router.get("/admin-only")
def admin_route(current_user: User = Depends(get_current_active_superuser),):
    return {"message": "Acceso permitido"}