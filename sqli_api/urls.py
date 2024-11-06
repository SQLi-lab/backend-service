from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('',  RedirectView.as_view(url='/check_user/', permanent=False)),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('check_user/', views.check_user, name='check')
]