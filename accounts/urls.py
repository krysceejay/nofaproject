from django.urls import path
from accounts.views import LoginView, RegisterView, DashboardView, LogoutView

urlpatterns = [
    path('login', LoginView.as_view()),
    path('register', RegisterView.as_view()),
    path('dashboard', DashboardView.as_view()),
    path('logout', LogoutView.as_view()),
]