from ninja import NinjaAPI

from .auth import JWTAuth, OAuth2Auth, auth_router

api = NinjaAPI()

# 認証関連のルーターを登録
api.add_router("/auth/", auth_router)


# 通常のAPIエンドポイント（JWTで保護）
@api.get("/protected", auth=JWTAuth())
def protected_endpoint(request):
    return {"message": f"Hello, {request.auth.username}!"}


# OAuth2で保護されたエンドポイント
@api.get("/oauth2-protected", auth=OAuth2Auth())
def oauth2_protected_endpoint(request):
    return {"message": f"OAuth2 authenticated as {request.auth.username}"}
