from ninja import Schema
from uuid import UUID
from typing import Optional
from datetime import datetime

from ..schemas.files_schemas import MessageResponse 
from ..schemas.types import StrongPassword

class ProfileOut(Schema):
    id: UUID
    email: str
    user_name: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    used_storage: int
    storage_limit: int
    created_at: datetime

class ProfileUpdateIn(Schema):
    full_name: Optional[str] = None


class ProfileResponse(MessageResponse):
    data: ProfileOut

class PasswordRequest(Schema):
    old_password: str
    new_password: StrongPassword