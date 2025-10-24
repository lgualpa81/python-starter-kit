from pydantic import BaseModel, ConfigDict

class Token(BaseModel):
    access_token: str
    token_type: str = 'Bearer'

class TokenData(BaseModel):
    sub: str
    username: str

class UserPublic(BaseModel):
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)