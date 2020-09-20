from django.shortcuts import render
from django.views.generic import View,TemplateView
from django.http import HttpResponse

# Create your views here.
class LoginView(TemplateView):
    template_name = 'accounts/login.html'

class RegisterView(TemplateView):
    template_name = 'accounts/register.html'

class DashboardView(TemplateView):
    template_name = 'accounts/dashboard.html'  

class LogoutView(TemplateView):
    template_name = 'accounts/dashboard.html'      
    
