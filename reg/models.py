from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Создание нового пользователя с заданным email и паролем."""
        if not email:
            raise ValueError("Email должен быть указан.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создание суперпользователя с заданным email и паролем."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=False)  # Поле email, обязательное и уникальное
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # Поле для суперпользователя

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Уникальное имя для обратной ссылки
        blank=True,
        help_text='Группы, к которым принадлежит пользователь.',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Уникальное имя для обратной ссылки
        blank=True,
        help_text='Специфические разрешения для этого пользователя.',
        related_query_name='customuser',
    )

    USERNAME_FIELD = 'email'  # Используем email как имя пользователя
    REQUIRED_FIELDS = []  # Оставьте пустым, если не требуется дополнительных полей

    objects = CustomUserManager()

    def __str__(self):
        return self.email
