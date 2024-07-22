from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import AbstractBaseUser,User

from myapp.models import Contactus, Profile


# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')


class ContactusForm(forms.ModelForm):
    class Meta:
        model = Contactus
        fields = ['name', 'email', 'subject', 'message']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']



class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )