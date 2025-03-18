from typing import Optional

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from pydantic import BaseModel, EmailStr, validator


# PydanticモデルでリクエストとレスポンスのスキーマをJSON形式で定義
class UserIn(BaseModel):
    username: str
    email: EmailStr
    password: str

    @validator("password")
    def password_validation(cls, v):
        try:
            validate_password(v)
        except ValidationError as e:
            raise ValueError(str(e))
        return v


class LoginIn(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None


class UserOut(BaseModel):
    id: int
    username: str
    email: str
