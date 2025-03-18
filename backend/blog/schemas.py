from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class BlogEntryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)


class BlogEntryCreate(BlogEntryBase):
    pass


class BlogEntryUpdate(BlogEntryBase):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)


class BlogEntryResponse(BlogEntryBase):
    id: int
    author_id: int
    author_username: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    content: str = Field(..., min_length=1)


class CommentCreate(CommentBase):
    blog_entry_id: int


class CommentUpdate(CommentBase):
    content: Optional[str] = Field(None, min_length=1)


class CommentResponse(CommentBase):
    id: int
    blog_entry_id: int
    author_id: int
    author_username: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BlogEntryDetailResponse(BlogEntryResponse):
    comments: List[CommentResponse]
