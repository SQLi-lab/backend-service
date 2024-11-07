import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, study_group, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email должен быть указан')
        email = self.normalize_email(email)
        user = self.model(username=username, study_group=study_group, email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, study_group, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, study_group, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('ФИО'), max_length=150, unique=False)
    study_group = models.CharField(_('Номер группы'), max_length=50)
    group = models.CharField(_('Группа'), max_length=120, default='student')
    email = models.EmailField(_('email'), unique=True)
    verified = models.BooleanField(_('Подтвержден'), default=False)
    is_active = models.BooleanField(_('Активен'), default=True)
    is_staff = models.BooleanField(_('Статус персонала'), default=False)
    is_superuser = models.BooleanField(_('Суперпользователь'), default=False)
    date_joined = models.DateTimeField(_('Дата регистрации'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'study_group']

    def __str__(self):
        return self.email

class Lab(models.Model):
    STATUS_CHOICES = [
        ('Создается', 'Создается'),
        ('Ошибка создания', 'Ошибка создания'),
        ('Создана', 'Создана'),
        ('Остановлена', 'Остановлена'),
        ('Решена', 'Решена'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    url = models.URLField(unique=True, blank=True, null=True)
    unique_secret_hash = models.CharField(max_length=1024, unique=True)

    expired_seconds = models.IntegerField(null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(default=False)
    date_done = models.DateTimeField(blank=True, null=True)

    status = models.CharField(choices=STATUS_CHOICES,
                              default='Создается',
                              max_length=50)
