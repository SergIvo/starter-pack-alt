from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.password_validation import validate_password
from django.db import models


class UserManager(BaseUserManager):
    """Менеджер авторизации для пользователей."""

    @classmethod
    def normalize_username(cls, username):
        return username.lower()

    def _create_user(self, email, last_name, first_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Не указан адрес электронной почты.')
        if not last_name:
            raise ValueError('Не указана фамилия.')
        if not first_name:
            raise ValueError('Не указано имя.')

        email = self.normalize_username(email)
        user = self.model(email=email, last_name=last_name, first_name=first_name, **extra_fields)
        validate_password(password, user)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, last_name, first_name, password=None, **extra_fields):
        """Создает и возвращает `User` с адресом электронной почты, Ф.И. пользователя и паролем."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, last_name, first_name, password, **extra_fields)

    def create_superuser(self, email, last_name, first_name, password, **extra_fields):
        """Создает и возвращает пользователя с правами суперпользователя (администратора)."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self._create_user(email, last_name, first_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Пользователь системы."""

    email = models.EmailField('Электронная почта', max_length=255, null=False, blank=False, unique=True)
    is_staff = models.BooleanField('Признак отношения к персоналу', default=False)
    is_active = models.BooleanField('Признак активности', default=True)
    last_name = models.CharField('Фамилия', max_length=25)
    first_name = models.CharField('Имя', max_length=25)

    objects = UserManager()

    REQUIRED_FIELDS = ['last_name', 'first_name', 'password']
    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """Возвращает строковое представление пользователя."""
        return f'{self.first_name} {self.last_name}'
