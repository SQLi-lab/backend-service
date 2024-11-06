from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, group, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email должен быть указан')
        email = self.normalize_email(email)
        user = self.model(username=username, group=group, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, group, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, group, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('ФИО'), max_length=150, unique=False)
    group = models.CharField(_('Номер группы'), max_length=50)
    email = models.EmailField(_('email'), unique=True)
    verified = models.BooleanField(_('Подтвержден'), default=False)
    is_active = models.BooleanField(_('Активен'), default=True)
    is_staff = models.BooleanField(_('Статус персонала'), default=False)
    date_joined = models.DateTimeField(_('Дата регистрации'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'group']

    def __str__(self):
        return self.email
