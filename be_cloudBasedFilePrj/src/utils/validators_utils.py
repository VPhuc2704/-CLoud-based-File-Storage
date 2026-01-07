import re

def to_title_case(v: str) -> str:
    return v.title()

def validate_no_digits(v: str) -> str:
    if any( char.isdigit() for char in v):
        raise ValueError("Họ tên không được chứa ký tự số")
    return v

def no_whilespace(v: str) -> str:
    """UserName khong được chứa khoảng trắng"""
    if any(c.isspace() for c in v):
        raise ValueError("Username không được chứa ký tự trắng")
    return v

def check_strong_pass(v: str) -> str:
    """Mật khẩu: 8 ký tự, 1 hoa, 1 thường, 1 số, 1 ký tự đặc biệt"""
    if len(v) < 8:
        raise ValueError("Mật khẩu phải từ 8 ký tự trở lên.")
    if not re.search(r"[A-Z]", v):
        raise ValueError("Thiếu chữ in hoa.")
    if not re.search(r"[a-z]", v):
        raise ValueError("Thiếu chữ thường.")
    if not re.search(r"\d", v):
        raise ValueError("Thiếu số.")
    if not re.search(r"[!@#$%^&*()]", v):
        raise ValueError("Thiếu ký tự đặc biệt.")
    return v

