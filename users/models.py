from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager # Импортируем базовый UserManager
from django.db import models

# 1. Создаем кастомный менеджер пользователей
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True) # Обычно суперпользователи всегда активны

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # отключаем username
    email = models.EmailField('Email address', unique=True)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Больше не нужен email, так как он USERNAME_FIELD, и username нет

    # 2. Назначаем кастомный менеджер нашей модели User
    objects = CustomUserManager()

    def __str__(self):
        return self.email