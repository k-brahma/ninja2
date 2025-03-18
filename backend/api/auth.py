import datetime
from typing import Optional

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponse
from ninja import Router
from ninja.security import HttpBearer
from oauth2_provider.models import AccessToken
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


# JWT認証のためのベアラートークン認証クラス
class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if user_id:
                user = User.objects.get(id=user_id)
                return user
        except (jwt.PyJWTError, User.DoesNotExist):
            pass
        return None


# OAuth2認証クラス
class OAuth2Auth(HttpBearer):
    def authenticate(self, request, token):
        try:
            access_token = AccessToken.objects.get(token=token)
            if not access_token.is_expired():
                return access_token.user
        except AccessToken.DoesNotExist:
            pass
        return None


# 認証関連のルーター
auth_router = Router()


@auth_router.post("/register", response=UserOut)
def register(request, data: UserIn):
    """新規ユーザー登録エンドポイント"""
    with transaction.atomic():
        user = User.objects.create_user(
            username=data.username, email=data.email, password=data.password
        )
    return user


@auth_router.post("/login", response=TokenOut)
def login(request, data: LoginIn):
    """ログインエンドポイント - JWTトークンを発行"""
    user = authenticate(username=data.username, password=data.password)
    if user is None:
        return HttpResponse("Invalid credentials", status=401)

    # JWTトークン生成
    expiry = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {"user_id": user.id, "exp": expiry}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return {"access_token": token, "token_type": "bearer", "expires_in": 3600}  # 1時間


@auth_router.post("/logout")
def logout(request, data: TokenOut):
    """ログアウトエンドポイント - 必要に応じてトークン無効化など実装"""
    # JWTの場合はクライアント側でのトークン削除が一般的だが、
    # 必要に応じてブラックリスト機能を実装することも可能
    return {"success": True}


@auth_router.get("/me", response=UserOut, auth=JWTAuth())
def get_user(request):
    """現在のユーザー情報を取得"""
    return request.auth  # JWTAuthクラスによって認証されたユーザー
