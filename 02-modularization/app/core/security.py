import os
import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError, ExpiredSignatureError

from app.models.user import UserORM
from app.api.v1.auth.repository import UserRepository

from .config import settings
from .db import get_db
from .constants import RoleEnum

# SECRET_KEY = os.getenv("SECRET_KEY", "t0pS3c3T123")
# ALGORITHM = "HS256"
# EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login", scheme_name="JWT")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unauthorized",
    headers={"WWW-Authenticate": "Bearer"},
)


def raise_expired_token():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )


def raise_forbidden_token():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient permissions",
    )


def invalid_credentials():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
    )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + \
        (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(claims=to_encode, key=settings.JWT_SECRET,
                       algorithm=settings.JWT_ALGORITHM)
    return token


def decode_token(token: str) -> dict:
    return jwt.decode(token=token, key=settings.JWT_SECRET,
                      algorithms=[settings.JWT_ALGORITHM])


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> UserORM:
    try:
        payload = decode_token(token)
        sub: Optional[str] = payload.get("sub")

        if not sub:
            raise credentials_exception
        user_id = int(sub)
    except ExpiredSignatureError:
        raise raise_expired_token()
    except JWTError as e:
        raise credentials_exception

    user = db.get(UserORM, user_id)
    if not user or not user.is_active:
        raise invalid_credentials()

    return user


def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    try:
        plain_bytes = plain.encode('utf-8')
        hashed_bytes = hashed.encode('utf-8')
        return bcrypt.checkpw(plain_bytes, hashed_bytes)
    except (ValueError, Exception):
        return False


def require_role(min_role: RoleEnum):
    order = {role.name: role.value for role in RoleEnum}

    def evaluation(user: UserORM = Depends(get_current_user)) -> UserORM:
        if order.get(user.role.name) < order.get(min_role):
            raise raise_forbidden_token()
        return user
    return evaluation


async def auth2_token(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    repository = UserRepository(db)
    user = repository.get_by_email(form.username)
    if not user or not verify_password(form.password, user.hashed_password):
        raise invalid_credentials()
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

require_user = require_role("user")
require_editor = require_role("editor")
require_admin = require_role("admin")
