from django.urls import path
from django.views.generic import RedirectView

from .routes.admin import admin_help, admin_users, admin_user_verify, \
    admin_user_delete, admin_labs_dump, admin_users_dump
from .routes.labs import lab_add, labs, lab_info, lab_delete, labs_stats, \
    lab_check, admin_labs
from .routes.login import login_view, logout_view, register_view
from .routes.user import my_account
from .routes.help import help

urlpatterns = [
    path('',  RedirectView.as_view(url='/labs/', permanent=False)),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

    path('labs/<uuid:uuid>/delete', lab_delete, name='lab_delete'),
    path('labs/<uuid:uuid>/check', lab_check, name='lab_check'),
    path('labs/<uuid:uuid>', lab_info, name='lab_info'),
    path('labs/stats', labs_stats, name='lab_stats'),
    path('labs/add/', lab_add, name='lab_add'),
    path('labs/', labs, name='labs'),

    path('my_account', my_account, name='my_account'),

    path('help', help, name='help'),

    path('admin/help', admin_help, name='admin_help'),
    path('admin/users/<uuid:uuid>/verify', admin_user_verify, name='admin_user_verify'),
    path('admin/users/<uuid:uuid>/delete', admin_user_delete, name='admin_user_delete'),
    path('admin/users', admin_users, name='admin_users'),
    path('admin/labs', admin_labs, name='admin_labs'),
    path('admin/dump/labs', admin_labs_dump, name='admin_labs_dump'),
    path('admin/dump/users', admin_users_dump, name='admin_users_dump'),
]