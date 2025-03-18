from typing import List

from auth_api.api import JWTAuth
from django.http import HttpRequest
from ninja import NinjaAPI, Router
from ninja.pagination import paginate

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

# NinjaAPI インスタンスの作成
api = NinjaAPI()

# メインのブログルーター
router = Router()


@router.get("/", response=List[BlogEntryResponse])
@paginate
def list_blog_entries(request):
    return BlogEntry.objects.all()


@router.get("/{entry_id}", response=BlogEntryDetailResponse)
def get_blog_entry(request, entry_id: int):
    entry = BlogEntry.objects.get(id=entry_id)
    return entry


@router.post("/", response=BlogEntryResponse, auth=JWTAuth())
def create_blog_entry(request, payload: BlogEntryCreate):
    entry = BlogEntry.objects.create(
        title=payload.title, content=payload.content, author=request.auth
    )
    return entry


@router.put("/{entry_id}", response=BlogEntryResponse, auth=JWTAuth())
def update_blog_entry(request, entry_id: int, payload: BlogEntryUpdate):
    entry = BlogEntry.objects.get(id=entry_id)

    # 認証済みユーザーが作者であることを確認
    if entry.author != request.auth:
        return router.api.create_response(request, {"detail": "Not authorized"}, status=403)

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(entry, attr, value)
    entry.save()
    return entry


@router.delete("/{entry_id}", auth=JWTAuth())
def delete_blog_entry(request, entry_id: int):
    entry = BlogEntry.objects.get(id=entry_id)

    # 認証済みユーザーが作者であることを確認
    if entry.author != request.auth:
        return router.api.create_response(request, {"detail": "Not authorized"}, status=403)

    entry.delete()
    return {"success": True}


# コメント用のルーター
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
        return router.api.create_response(request, {"detail": "Not authorized"}, status=403)

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(comment, attr, value)
    comment.save()
    return comment


@comment_router.delete("/{comment_id}", auth=JWTAuth())
def delete_comment(request, blog_id: int, comment_id: int):
    comment = Comment.objects.get(id=comment_id, blog_entry_id=blog_id)

    # 認証済みユーザーが作者であることを確認
    if comment.author != request.auth:
        return router.api.create_response(request, {"detail": "Not authorized"}, status=403)

    comment.delete()
    return {"success": True}


# コメントルーターをブログルーターに登録
router.add_router("/{blog_id}/comments/", comment_router)


# APIに直接登録するための関数
def register_api_routes(api: NinjaAPI) -> None:
    """
    APIにブログ関連のルートを登録します。
    これは、メインのAPI設定で呼び出されます。
    """
    api.add_router("/blog", router)
