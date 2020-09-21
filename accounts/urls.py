from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm

app_name = 'accounts'

urlpatterns = [
    path('login/', 
    auth_views.LoginView.as_view(
        template_name='registration/login.html', 
        authentication_form=UserLoginForm
        ), 
    name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
]