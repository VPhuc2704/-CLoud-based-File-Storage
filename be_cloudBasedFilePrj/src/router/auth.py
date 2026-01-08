from ninja import Router
from ninja.responses import Response
from ninja.errors import ValidationError

from ..schemas.auth_schemas import (
    RegisterRequest, LoginRequest,
    LoginResponse, MessageResponse, TokenResponse
)
from ..services import auth_service
from django.conf import settings


router = Router(tags=["Auth"])
auth_service = auth_service.AuthService()

@router.post("/register", response={201: MessageResponse})
def register(request, payload: RegisterRequest):

    auth_service.register(
        user_name=payload.user_name,
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name
    )
    return 201, {
        "success": True,
        "message": "Đăng ký thành công"
    }


@router.post("/login", response={200: LoginResponse})
def login(request, payload: LoginRequest):
    result = auth_service.login(
        user_name=payload.user_name, 
        password=payload.password
    )
    
    response_data = Response(
        {
            "success": True,
            "user": {
                "id": str(result["user"].id),
                "email": result["user"].email,
                "fullName": result["user"].full_name,
                "userName": result["user"].user_name,
                "avatarUrl": result["user"].avatar_url,
                "isActive": result["user"].is_active
            },
            "tokens": {
                "token_type": "bearer",
                "access_token": result["access_token"]
            }
        }
    )


    response_data.set_cookie(
        "refresh_token",
        result["refresh_token"],
        httponly=True,
        secure=False,
        samesite="Lax",
        domain=None,
        max_age=24 * 3600 * settings.REFRESH_EXP_DAYS,
    )

    return response_data


@router.post("/refresh", response={200: TokenResponse})
def refresh(request):
    refresh_token = request.COOKIES.get("refresh_token")
    
    if not refresh_token:
        return 401, {"detail": "Không có refresh token"}

    try:
        new_access_token = auth_service.refresh_token(refresh_token)
        return {
            "token_type": "Bearer",
            "access_token": new_access_token
        }
    except ValidationError as e:
        return 401, {"detail": str(e)}


@router.post("/logout", response={200: MessageResponse})
def logout(request):
    try:
        refresh_token = request.COOKIES.get("refresh_token")
        auth_service.logout(refresh_token)

        response = Response(
            {
                "success": True,
                "message": "Đăng xuất thành công"
            }
        )
        response.delete_cookie("refresh_token")
        return response

    except Exception as e:
        return 400, {"detail": str(e)}