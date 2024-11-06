from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'group', 'verified', 'is_active', 'is_staff', 'is_superuser', 'date_joined')

    # Фильтрация по полям
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'group')

    # Поля, которые показываются в форме редактирования пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'group', 'verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Поля, которые показываются при добавлении нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'group', 'verified', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'username', 'group')
    ordering = ('email',)

# Регистрируем CustomUser в админке
admin.site.register(CustomUser, CustomUserAdmin)
