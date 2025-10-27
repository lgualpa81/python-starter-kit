from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_current_user, oauth2_scheme, hash_password, verify_password, require_admin, auth2_token
from app.core.db import get_db
from app.models.user import UserORM

from .schemas import TokenResponse, UserPublic, UserCreate, UserLogin, RoleUpdate
from .repository import UserRepository

# FAKE_USERS = {
#     "joe": {"email": "joe@demo.io", "username": "joe", "password": "12345678"},
# }

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> UserPublic:
    repository = UserRepository(db)
    email, password, full_name = payload.email.strip().lower(
    ), payload.password.strip(), payload.full_name.strip()
    if repository.get_by_email(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Account already exists")
    user = repository.create(
        email=email,
        hashed_password=hash_password(password),
        full_name=full_name
    )
    db.commit()
    db.refresh(user)
    return UserPublic.model_validate(user)


# @router.post("/login", response_model=Token)
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = FAKE_USERS.get(form_data.username, None)
#     if not user or user.get("password") != form_data.password:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid credentials",
#         )
#     access_token = create_access_token(
#         data={"sub": user.get("email"), "username": user.get("username")},
#         expires_delta=timedelta(minutes=30)
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=TokenResponse)
async def login(
        # payload: Optional[UserLogin] = None,
        payload: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    # if payload:
    #     email, password = payload.email.lower(), payload.password
    # elif form_data:
    email, password = payload.username, payload.password
    # else:
    #     raise HTTPException(status_code=400, detail="No credentials provided")

    repository = UserRepository(db)
    user = repository.get_by_email(email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=token, user=UserPublic.model_validate(user))


@router.get("/me", response_model=UserPublic)
async def read_me(current: UserORM = Depends(get_current_user)):
    return {"email": current.email, "id": current.id, "role": current.role, "is_active": current.is_active}


@router.get("/secure")
def secure_endpoint(token: str = Depends(oauth2_scheme)):
    return {"message": "Token allowed access", "token_recibido": token}


@router.put("/role/{user_id}", response_model=UserPublic)
def set_role(
    user_id: int = Path(..., ge=1),
    payload: RoleUpdate = None,
    db: Session = Depends(get_db),
    _admin: UserORM = Depends(require_admin)
):
    repository = UserRepository(db)
    user = repository.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    updated = repository.set_role(user, payload.role)

    db.commit()
    db.refresh(updated)
    return UserPublic.model_validate(updated)


@router.post("/token")
async def token_endpoint(response=Depends(auth2_token)):
    return response
