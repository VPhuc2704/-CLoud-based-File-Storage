from ninja import Field, Schema
from typing import Optional

# Input Schemas
class RegisterRequest(Schema):
    user_name: str
    full_name: str
    email: str
    password: str

class LoginRequest(Schema):
    user_name: str
    password: str

class RefreshTokenRequest(Schema):
    refresh_token: str

class TokenResponse(Schema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserInfoResponse(Schema):
    id: str
    user_name: str = Field(..., alias="userName")
    email: str 
    full_name: Optional[str] = Field(None, alias="fullName")
    avatar_url: Optional[str] = Field(None, alias="avatarUrl")
    is_active: bool = Field(..., alias="isActive")

class LoginResponse(Schema):
    user: UserInfoResponse
    tokens: TokenResponse

class MessageResponse(Schema):
    success  : bool
    message: str