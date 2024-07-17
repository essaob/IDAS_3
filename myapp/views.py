
from django import forms
from django.contrib.auth.models import User

from .forms import PortfolioForm, CustomUserCreationForm, CustomLoginForm
from django.contrib.auth import login as auth_login, authenticate
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .models import CustomUser
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, mail_admins
from .forms import ContactUsForm
from django.http import HttpResponse
from .models import Project

from django.contrib import messages
# from .forms import RegisterUserForm

# Create your views here.
def chatPage(request):
    return render(request,'chatPage.html')

# class RegisterUserForm(UserCreationForm):
#     email = forms.EmailField()
#     first_name = forms.CharField(max_length=50)
#     last_name = forms.CharField(max_length=50)
#     class Meta:
#         model = CustomUser
#
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
@login_required
def home(request):
    """
    Home page func
    Get request and retrun home page
    """
    return render(request, 'chatPage.html')



@login_required
def personalArea(request):
    return render(request, 'personalArea.html')


@login_required
def logoutuser(request):  # p
    if request.method == 'POST':  # method post!!!
        logout(request)
        return redirect('chatPage')  # return home page after logout


@login_required
def userSettings(request):
    user = get_object_or_404(User, request.user.id)
    if request.method == 'GET':
        form = User(user)
        return render(request, 'userSettings.html', {'user': user, 'form': form})
    else:
        try:
            form = User(request.POST, user)
            form.save(user)
            if validator(request.POST['password1'], request.POST['password2']):
                user.set_password(request.POST['password1'])
                user.save()
            return redirect('personalArea')
        except ValueError:
            return render(request, 'userSettings.html', {'user': user, 'form': form, 'error': 'Bad info'})
#

def validator(val1, val2):
    if val1 != '' and val1 == val2:
        return True
    return False


class RegisterUserForm:
    pass


def signupuser(request):
    """
    Sign up func

    """
    # if request.method == "POST":
    #     form = RegisterUserForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         username = form.cleaned_data['username']
    #         password = form.changed_data['password1']
    #         try:
    #             user = authenticate(username= username, password= password)
    #             user.save()
    #             login(request, user)
    #             messages.success(request, ("Registration Successful!"))
    #             return redirect('home')
    #         except IntegrityError :
    #             return render(request, 'signupuser.html', {'form':RegisterUserForm(), 'error':'That username has already been taken.Please try again'})
    #     else:
    #         form = RegisterUserForm()
    #         return render(request, 'signupuser.html', {'form':form})
    # else:
    #     return render(request, 'signupuser.html', {'form':RegisterUserForm()})

    if request.method == 'GET':
        return render(request, 'signupuser.html', {'form': RegisterUserForm()})  # User creation form
    else:
        if request.POST['password1'] == request.POST['password2']:  # if first and second password equal create new user
            try:
                user = UserCreationForm.objects.create_user(request.POST['username'], password=request.POST['password1'],
                                                      first_name=request.POST['first_name'],
                                                      last_name=request.POST['last_name'],
                                                       email=request.POST['email'])
                                                      # create user
                user.save()  # save user
                login(request, user)
                messages.success(request, ("Registartion Successful!"))
                return redirect('chatPage')  # return current page
            except IntegrityError:
                return render(request, 'signupuser.html', {'form': RegisterUserForm(),
                                                           'error': 'That username has already been taken.Please try again'})
                # if user create login that exist send error massege
        else:
            return render(request, 'signupuser.html', {'form': RegisterUserForm(), 'error': 'Passwords did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'loginuser.html', {'form': AuthenticationForm()})  # Authentication Form
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('chatPage')  # return current page


def contactus(request):
    """
    Contact US func
    Get request and return contactus page
    """
    if request.method == 'GET':
        return render(request, 'contactus.html')
    else:
        form = ContactUsForm(request.POST)
        message = 'Message was sent successfully'
        hasError = False
        if form.is_valid():
            form.save()
            form = ContactUsForm()
            form.fields['name'] = ''
            form.fields['email'] = ''
            form.fields['subject'] = ''
            form.fields['message'] = ''
            recipients = ['alobraessa2212@gmail.com']
            subject = request.POST.get('subject', '')
            message = request.POST.get('message', '')
            from_email = request.POST.get('email', '')
            send_mail(subject, message, from_email, recipients)
        else:
            hasError = True
            message = 'Please make sure all fields are valid'

    return render(request, 'contactus.html', {'form': form, 'message': message, 'hasError': hasError})

#
# def contactadmin(request):
#     """
#     Contact US func
#     Get request and return contactus page
#     """
#     if request.method == 'GET':
#         return render(request, 'contactadmin.html')
#     else:
#         form = ContactAdminForm(request.POST)
#         message = 'Message was sent successfully'
#         hasError = False
#         if form.is_valid():
#             form = ContactAdminForm(request.POST)
#             form.save()
#             # form.fields['subject'] = ''
#             # form.fields['message'] = ''
#             # subject = request.POST['subject']
#             # message = request.POST['message']
#             # mail_to_admin = ContactAdmin(subject =subject,message = message)
#             # mail_to_admin.save()
#
#         else:
#             hasError = True
#             message = 'Please make sure all fields are valid'
#
#     return render(request, 'contactus.html', {'form': form, 'message': message, 'hasError': hasError})
#

def base(request):
    return render(request,'base.html')



@login_required
def userPortfolio(request):  # p
    projects = Project.objects.filter(user=request.user)
    return render(request, 'userPortfolio.html', {'projects': projects})


@login_required
def detailp(request, project_id):
    project = get_object_or_404(Project, pk=project_id, user=request.user)
    return render(request, 'detailp.html', {'project': project})


@login_required
def createPortfolio(request):
    if request.method == 'GET':
        return render(request, 'createPortfolio.html')
    else:
        try:
            form = PortfolioForm(request.POST, request.FILES)  # edit form
            newPortfolio = form.save(commit=False)  # save all input data in database
            newPortfolio.user = request.user
            newPortfolio.save()  # save data
            return redirect('userPortfolio')
        except ValueError:
            return render(request, 'createPortfolio.html',
                          {'form': PortfolioForm(), 'error': 'Bad data passed in. Try again'})


@login_required
def editProject(request, project_id):
    project = get_object_or_404(Project, pk=project_id, user=request.user)
    if request.method == 'GET':
        form = PortfolioForm(instance=project)
        return render(request, 'editProject.html', {'project': project, 'form': form})
    else:
        try:
            form = PortfolioForm(request.POST, instance=project)
            form.save(project)
            return redirect('detailp', project_id)
        except ValueError:
            return render(request, 'editProject.html', {'project': project, 'form': form, 'error': 'Bad info'})


@login_required
def deleteProject(request, project_id):  # delete can do only user who create todo
    project = get_object_or_404(Project, pk=project_id,
                                user=request.user)  # find todo in database(import get_object_or_404), (user=request.user) check if todo belongs to user
    if request.method == 'POST':  # Post becouse we upload data to database
        Project.delete(project)  # delete blog
        return redirect('userPortfolio')  # return page with current todos




def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('base')  # Redirect to some page after signup
    else:
        form = UserCreationForm()
    return render(request, 'signupuser.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('base')  # Redirect to some page after login
    else:
        form = AuthenticationForm()
    return render(request, 'loginuser.html', {'form': form})