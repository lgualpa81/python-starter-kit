from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .schemas import Token, UserPublic
from app.core.security import create_access_token, get_current_user, oauth2_scheme

FAKE_USERS = {
    "joe": {"email": "joe@demo.io", "username":"joe", "password":"12345678"},
}

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = FAKE_USERS.get(form_data.username, None)
    if not user or user.get("password") != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    access_token = create_access_token(
        data = {"sub": user.get("email"), "username": user.get("username")},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserPublic)
async def read_me(current=Depends(get_current_user)):
    return {"email": current.get("email"), "username": current.get("username")}

@router.get("/secure")
def secure_endpoint(token: str = Depends(oauth2_scheme)):
    return {"message": "Acceso con token", "token_recibido": token}