from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control', 
            'placeholder': 'user name', 
            'id': 'login-username'
            }
        ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control', 
            'placeholder': 'password', 
            'id': 'login-password'
            }
        ))

class UserRegistrationForm(forms.ModelForm): 
    username = forms.CharField(
        label='Enter User name', min_length=4, max_length=50, help_text='Required'
    ) 
    email = forms.EmailField(
        label='Enter Email', max_length=100, help_text='Required', error_messages={
            'required': 'Sorry you will need an email'
        }
    )  
    password = forms.CharField(label='Enter Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput) 

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',)

    def clean_username(self):
        username = self.cleaned_data['username'].lower() 
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exist")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower() 
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already taken")
        return email    

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']: 
            raise forms.ValidationError("Passwords do not match")
        return cd['password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Username'}
        )
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Email'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Password'}
        ) 
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'}
        )       