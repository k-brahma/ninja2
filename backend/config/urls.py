from auth_api.api import auth_router
from blog.api import register_api_routes
from django.contrib import admin
from django.urls import include, path
from ninja import NinjaAPI

# メインAPIインスタンスの作成
api = NinjaAPI()

# 認証関連のルーターを登録
api.add_router("/auth", auth_router)

# ブログ関連のルーターを登録
register_api_routes(api)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path(
        "o/", include("oauth2_provider.urls", namespace="oauth2_provider")
    ),  # OAuth2エンドポイント
]
