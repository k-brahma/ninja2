import datetime

import jwt
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.db import transaction
from django.http import HttpResponse
from ninja import Router
from ninja.security import HttpBearer
from oauth2_provider.models import AccessToken

from .schemas import LoginIn, TokenOut, UserIn, UserOut

# カスタムユーザーモデルを取得
User = get_user_model()


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
    # ユーザー名とメールアドレスの重複をチェック
    if User.objects.filter(username=data.username).exists():
        return HttpResponse("Username already exists", status=400)
    if User.objects.filter(email=data.email).exists():
        return HttpResponse("Email already exists", status=400)

    with transaction.atomic():
        user = User.objects.create_user(
            username=data.username, email=data.email, password=data.password
        )
    # Userオブジェクトから明示的にUserOutスキーマに合うディクショナリを作成して返す
    return {"id": str(user.id), "username": user.username, "email": user.email}


@auth_router.post("/login", response=TokenOut)
def login(request, data: LoginIn):
    """ログインエンドポイント - JWTトークンを発行"""
    user = authenticate(username=data.email, password=data.password)
    if user is None:
        return HttpResponse("Invalid credentials", status=401)

    # JWTトークン生成
    expiry = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {"user_id": str(user.id), "exp": expiry}  # UUIDをstr型に変換
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
    user = request.auth  # JWTAuthクラスによって認証されたユーザー
    return {"id": str(user.id), "username": user.username, "email": user.email}
