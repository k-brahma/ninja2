import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """UUIDフィールドをIDとして使用するカスタムユーザーモデル"""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ユーザーID"
    )

    # 将来的に追加できる追加フィールドの例
    # bio = models.TextField(blank=True, verbose_name="自己紹介")
    # birth_date = models.DateField(null=True, blank=True, verbose_name="生年月日")

    class Meta:
        verbose_name = "ユーザー"
        verbose_name_plural = "ユーザー"

    def __str__(self):
        return self.username
