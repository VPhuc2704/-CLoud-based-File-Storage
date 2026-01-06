from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.utils import timezone

import jwt
from datetime import timedelta

from src.models import Account, RefreshToken
from src.exceptions import InvalidCredentials, InvalidToken, PermissionDenied

def hash_password(password: str) -> str:
    return make_password(password)

def verify_password(password: str, hashed: str) -> bool:
    return check_password(password, hashed)

def create_access_tokens(account: Account):
    now = timezone.now()
    access_payload ={
        "user_id": str(account.id),
        "exp": now + timedelta(minutes=settings.ACCESS_EXPIRE_MINUTES),
        "type":"access_token"
    }
    access_token = jwt.encode(access_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return access_token

def create_resfresh_tokens(account: Account):
    now = timezone.now()
    exp_time = now + timedelta(days=settings.REFRESH_EXP_DAYS)
    refresh_payload ={
        "user_id": str(account.id),
        "exp": exp_time,
        "type":"refresh_token"
    }
    refresh_token = jwt.encode(refresh_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    RefreshToken.objects.create(
        account=account,
        token=refresh_token,
        revoked=False,
        expired_at= exp_time
    )
    return refresh_token 
    
def verify_refresh(token: str):
    """
    Xác thực token và trả về payload nếu hợp lệ,
    nếu không hợp lệ sẽ raise lỗi.
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )

        if payload.get("type") != "refresh_token":
            raise ValueError("Không phải refresh token")
        db_token = RefreshToken.objects.filter(token=token, revoked=False).first()
        if not db_token:
            raise ValueError("Refresh token bị thu hồi hoặc không tồn tại")
        if db_token.expired_at < timezone.now():
            raise ValueError("Refresh token đã hết hạn")
        return payload
    except jwt.ExpiredSignatureError:
        raise InvalidToken("Token đã hết hạn")
    except jwt.InvalidTokenError:
        raise InvalidToken("Token không hợp lệ")