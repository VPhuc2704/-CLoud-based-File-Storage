from ninja.security import HttpBearer
from ninja.errors import HttpError
from django.conf import settings

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from src.models import Account
from src.exceptions import InvalidToken, ResourceNotFound, PermissionDenied


class AuthBearer(HttpBearer):
    """
    Xác thực JWT token.
    1. Ninja tự động tách 'Bearer <token>' và truyền vào hàm authenticate.
    2. Cookie: access_token
    """

    def __call__(self, request):
        token = None 
        
        auth_header = request.headers.get("Authorization")

        if auth_header:
            if not auth_header.startswith("Bearer "):
                raise HttpError(401, "Invalid Authorization header")
            token = auth_header.replace("Bearer ", "", 1)

        if not token:
            token = request.COOKIES.get("access_token")

        if not token: 
            raise  HttpError(401, "Authentication token required")
        
        return self.authenticate(request, token)

    def authenticate(self, request, token):
        try:
            payload = jwt.decode(
                token, 
                settings.JWT_SECRET, 
                algorithms=[settings.JWT_ALGORITHM]
            )

            if payload.get("type") != "access_token":
                raise InvalidToken(401, "Token không hợp lệ (Cần Access Token)")

            user_id = payload.get("user_id")
            if not user_id:
                raise InvalidToken(401, "Token payload bị lỗi")

            try:
                account = Account.objects.get(id=user_id)
            except Account.DoesNotExist:
                raise ResourceNotFound(401, "Người dùng không tồn tại")

            request.user = account
            return account

        except ExpiredSignatureError:
            raise InvalidToken(401, "Token has expired")
        except InvalidTokenError:
            raise InvalidToken(401, "Invalid token")
        except Exception:
            raise InvalidToken(401, "Authentication Failed")
