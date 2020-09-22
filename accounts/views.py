from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required 
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserEditForm
from .token import account_activation_token

# Create your views here.
class LoginView(View):
    template_name = 'accounts/login.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class RegisterView(View):
    template_name = 'accounts/register.html'

class DashboardView(View):
    template_name = 'accounts/dashboard.html'  

class LogoutView(View):
    template_name = 'accounts/dashboard.html' 

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html', {'section': 'dashboard'}) 


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request,
                  'accounts/edituser.html',
                  {'user_form': user_form})


def register(request):
    if request.method == 'POST':
        registerForm = UserRegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('Registered successfully. Please check your email to active your account.')
    else:
        registerForm = UserRegistrationForm()
        return render(request, 'registration/register.html', {'form': registerForm})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None 

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()    
        # login(request, user)
        return redirect('login')  
    else:
        return render(request, 'registration/activation_invalid.html')         

    
