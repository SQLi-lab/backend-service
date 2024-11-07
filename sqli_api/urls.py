from django.urls import path
from django.views.generic import RedirectView
from .routes.labs import lab_add, labs, lab_info, lab_delete
from .routes.login import login_view, logout_view, register_view, check_user

urlpatterns = [
    path('',  RedirectView.as_view(url='/labs/', permanent=False)),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('check_user/', check_user, name='check'),

    path('labs/<int:id>/delete', lab_delete, name='lab_delete'),
    path('labs/<int:id>', lab_info, name='lab_info'),
    path('labs/add/', lab_add, name='lab_add'),
    path('labs/', labs, name='labs'),
]