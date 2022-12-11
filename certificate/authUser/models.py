from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, null=True)
    login = models.CharField(max_length=150, unique=True)
    is_staff = models.BooleanField("staff status", default=False)
    is_active = models.BooleanField("active", default=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'login'

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return f"Login: {self.login}"
