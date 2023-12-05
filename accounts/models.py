from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, unique=True)
    realname = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, null=True, blank=True)
    regisNum = models.CharField(max_length=14)  # 주민등록번호 마스킹
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # groups와 user_permissions 필드에 대한 related_name 추가
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="Groups",
        blank=True,
        help_text="The groups this user belongs to.",
        related_name="custom_user_set",  # related_name 추가
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="User permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="custom_user_set",  # related_name 추가
        related_query_name="user",
    )

    def __str__(self):
        return self.username

