from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from myapp.models import  ContactUsModel ,ContactAdmin,Project
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import AbstractBaseUser,User


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUsModel
        fields = ["name", "email", "subject", "message"]

class ContactAdminForm(forms.ModelForm):
    class Meta:
        model = ContactAdmin
        fields = ["subject", "message"]


#
class UserSetting(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        # widgets={
        # 'password1':TextInput(attrs={'type':'password'})
        # }


class PortfolioForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'image', 'url']


class CustomLoginForm(AuthenticationForm):
    pass

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')



# class RegisterUserForm(UserCreationForm):
#     email = forms.EmailField()
#     first_name = forms.CharField(max_length=50)
#     last_name = forms.CharField(max_length=50)
#
#     class Meta:
#         model = CustomUser
#
#         fields = ('username', 'first_name', 'last_name', 'email',  'password1', 'password2')