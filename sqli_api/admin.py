from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Lab

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'study_group', 'group', 'verified', 'is_active', 'is_staff', 'is_superuser', 'date_joined')

    list_filter = ('is_staff', 'is_superuser', 'is_active', 'group')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'study_group', 'group', 'verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'study_group', 'group', 'verified', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'username', 'study_group', 'group')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

class LabAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'uuid', 'url', 'status', 'date_created', 'date_started', 'is_done', 'date_done')

    list_filter = ('status', 'is_done', 'date_created')

    search_fields = ('user__email', 'name', 'status')

    ordering = ('date_created',)

    fieldsets = (
        (None, {'fields': ('user', 'name', 'uuid', 'url', 'secret_hash', 'expired_seconds')}),
        ('Status & Dates', {'fields': ('status', 'date_created', 'date_started', 'is_done', 'date_done')}),
        ('Error log', {'fields': ('error_log',)}),
    )

admin.site.register(Lab, LabAdmin)
