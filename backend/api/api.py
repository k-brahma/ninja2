from typing import List

from ninja import NinjaAPI, Router
from ninja.pagination import paginate

from .auth import JWTAuth, OAuth2Auth, auth_router
from .models import BlogEntry, Comment
from .schemas import (
    BlogEntryCreate,
    BlogEntryDetailResponse,
    BlogEntryResponse,
    BlogEntryUpdate,
    CommentCreate,
    CommentResponse,
    CommentUpdate,
)

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


# Blog Entry endpoints
blog_router = Router()


@blog_router.get("/", response=List[BlogEntryResponse])
@paginate
def list_blog_entries(request):
    return BlogEntry.objects.all()


@blog_router.get("/{entry_id}", response=BlogEntryDetailResponse)
def get_blog_entry(request, entry_id: int):
    entry = BlogEntry.objects.get(id=entry_id)
    return entry


@blog_router.post("/", response=BlogEntryResponse, auth=JWTAuth())
def create_blog_entry(request, payload: BlogEntryCreate):
    entry = BlogEntry.objects.create(
        title=payload.title, content=payload.content, author=request.auth
    )
    return entry


@blog_router.put("/{entry_id}", response=BlogEntryResponse, auth=JWTAuth())
def update_blog_entry(request, entry_id: int, payload: BlogEntryUpdate):
    entry = BlogEntry.objects.get(id=entry_id)

    # 認証済みユーザーが作者であることを確認
    if entry.author != request.auth:
        return api.create_response(request, {"detail": "Not authorized"}, status=403)

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(entry, attr, value)
    entry.save()
    return entry


@blog_router.delete("/{entry_id}", auth=JWTAuth())
def delete_blog_entry(request, entry_id: int):
    entry = BlogEntry.objects.get(id=entry_id)

    # 認証済みユーザーが作者であることを確認
    if entry.author != request.auth:
        return api.create_response(request, {"detail": "Not authorized"}, status=403)

    entry.delete()
    return {"success": True}


# Comment endpoints
comment_router = Router()


@comment_router.get("/", response=List[CommentResponse])
@paginate
def list_comments(request, blog_id: int):
    return Comment.objects.filter(blog_entry_id=blog_id)


@comment_router.post("/", response=CommentResponse, auth=JWTAuth())
def create_comment(request, blog_id: int, payload: CommentCreate):
    comment = Comment.objects.create(
        content=payload.content, blog_entry_id=blog_id, author=request.auth
    )
    return comment


@comment_router.put("/{comment_id}", response=CommentResponse, auth=JWTAuth())
def update_comment(request, blog_id: int, comment_id: int, payload: CommentUpdate):
    comment = Comment.objects.get(id=comment_id, blog_entry_id=blog_id)

    # 認証済みユーザーが作者であることを確認
    if comment.author != request.auth:
        return api.create_response(request, {"detail": "Not authorized"}, status=403)

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(comment, attr, value)
    comment.save()
    return comment


@comment_router.delete("/{comment_id}", auth=JWTAuth())
def delete_comment(request, blog_id: int, comment_id: int):
    comment = Comment.objects.get(id=comment_id, blog_entry_id=blog_id)

    # 認証済みユーザーが作者であることを確認
    if comment.author != request.auth:
        return api.create_response(request, {"detail": "Not authorized"}, status=403)

    comment.delete()
    return {"success": True}


# ルーターの登録
api.add_router("/blog/", blog_router)
api.add_router("/blog/{blog_id}/comments/", comment_router)
