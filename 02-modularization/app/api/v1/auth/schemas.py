from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_serializer, field_validator
from typing import Optional
from app.core.constants import RoleEnum


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class UserPublic(UserBase):
    id: int
    role: RoleEnum
    is_active: bool

    @field_serializer('role')
    def serialize_role(self, role: RoleEnum) -> str:
        return role.name  # Retorna "user", "editor", "admin"


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=15)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    user: UserPublic


class RoleUpdate(BaseModel):
    role: RoleEnum = Field(..., description="Allowed roles: 'user', 'editor', 'admin'", examples=[
                           "user"])

    @field_validator("role", mode="before")
    def parse_role(cls, value):
        valid_values = [role.name for role in RoleEnum]
        # Si viene como string (ej: "user")
        if isinstance(value, str):
            try:
                return RoleEnum[value]
            except KeyError:
                raise ValueError(
                    f"Invalid role: '{value}'. Valid roles are: {', '.join(valid_values)}")
        # Si ya viene como int (ej: 0)
        if isinstance(value, int):
            try:
                return RoleEnum(value)
            except ValueError:
                raise ValueError(
                    f"Invalid role value: {value}. Valid numeric values are: "
                    f"{', '.join(str(r.value) for r in RoleEnum)} "
                    f"({', '.join(valid_values)})"
                )

    class Config:
        json_schema_extra = {
            "example": {
                "role": "user"
            }
        }


class TokenData(BaseModel):
    sub: str
    username: str

# class UserPublic(BaseModel):
#     username: str
#     email: str
#     model_config = ConfigDict(from_attributes=True)
