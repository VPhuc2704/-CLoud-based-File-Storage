from ninja import Router
from ninja.responses import Response
# Import schemas
from ..schemas.auth_schemas import (
    RegisterRequest, LoginRequest, RefreshTokenRequest,
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
    
    response_data = {
        "user": {
            "id": str(result["user"].id),
            "email": result["user"].email,
            "fullName": result["user"].full_name,
            "userName": result["user"].user_name,
            "avatarUrl": result["user"].avatar_url,
            "isActive": result["user"].is_active
        },
        "tokens": {
            "access_token": result["access_token"],
            "refresh_token":  result["refresh_token"],
            "token_type": "bearer"
        }
    }
    return response_data


@router.post("/refresh", response={200: TokenResponse})
def refresh(request, payload: RefreshTokenRequest):
    refresh_token = payload.refresh_token
    new_access_token = auth_service.refresh_token(refresh_token)
    
    return {
        "access_token": new_access_token,
        "refresh_token": payload.refresh_token,
        "token_type": "bearer"
    }


@router.post("/logout", response={200: MessageResponse})
def logout(request, payload: RefreshTokenRequest):
    refresh_token = payload.refresh_token
    auth_service.logout(refresh_token)

    return 200, {
        "success": True,
        "message": "Đăng xuất thành công"
    }