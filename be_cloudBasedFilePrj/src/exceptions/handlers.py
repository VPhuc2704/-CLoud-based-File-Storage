from ninja import NinjaAPI
from ninja.errors import ValidationError, HttpError
from django.http import JsonResponse
from .custom_exceptions import InvalidToken, PermissionDenied, BaseAppException

def global_exception_handlers(api: NinjaAPI):
    @api.exception_handler(BaseAppException)
    def handle_app_exception(request, exc):
        return JsonResponse({
            "success": False,
            "code": exc.code,
            "message": exc.message,
            "data": None,
            "details": exc.details
        }, status=exc.code)
    
    @api.exception_handler(ValidationError)
    def handle_validation_error(request, exc):
        if callable(getattr(exc, 'errors', None)):
            raw_errors = exc.errors()
        elif hasattr(exc, 'errors'):
            raw_errors = exc.errors
        else:
            raw_errors = str(exc)

        if isinstance(raw_errors, str):
            raw_errors = [raw_errors]

        clean_details = []
        for error in raw_errors:
            if isinstance(error, dict):
                loc = error.get('loc', [])
                field = str(loc[-1]) if loc else 'general'
                msg = error.get('msg', '').replace('Value error, ', '')
            else:

                field = 'general'
                msg = str(error)
            
            clean_details.append({
                "field": field,
                "message": msg
            })

        return JsonResponse({
            "success": False,
            "code": 422,
            "message": "Dữ liệu không hợp lệ",
            "data": None,
            "details": clean_details
        }, status=422)
    
    @api.exception_handler(HttpError)
    def handle_http_error(request, exc):
        return JsonResponse({
            "success": False,
            "code": exc.status_code,
            "message": str(exc),
            "data": None,
            "details": None
        }, status=exc.status_code)

    @api.exception_handler(Exception)
    def handle_general_exception(request, exc):
        return JsonResponse({
            "success": False,
            "code": 500,
            "message": "Lỗi hệ thống nội bộ",
            "data": None,
            "details": str(exc)
        }, status=500)