from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .forms import ContactusForm
from django.db import IntegrityError


# Create your views here.
def chatPage(request):
    return render(request,'chatPage.html')



@login_required
def logoutuser(request):
    logout(request)
    return redirect('loginuser')


def resetPassword(request):
    return render(request, 'resetPassword.html')


def signupuser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('loginuser')  # Redirect to login page after signup
    else:
        form = UserCreationForm()

    return render(request, 'loginuser.html', {'form': form})


def loginuser(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('chatPage')  # Redirect to the chat page after login
    else:
        form = AuthenticationForm()

    return render(request, 'loginuser.html', {'form': form})


def contactus(request):
    if request.method == 'GET':
        return render(request, 'contactus.html', {'form': ContactusForm()})
    else:
        form = ContactusForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Message was sent successfully'
            recipients = ['alobraessa2212@gmail.com']
            subject = request.POST.get('subject', '')
            message_body = request.POST.get('message', '')
            from_email = request.POST.get('email', '')
            send_mail(subject, message_body, from_email, recipients)
            form = ContactusForm()  # Reset the form after saving
        else:
            message = 'Please make sure all fields are valid'

        return render(request, 'contactus.html', {'form': form, 'message': message})


def base(request):
    return render(request,'base.html')


@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST['email']

        if 'profile_picture' in request.FILES:
            user.profile.profile_picture = request.FILES['profile_picture']

        user.save()
        from django.contrib import messages
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('profile')

    return render(request, 'profile.html', {'user': request.user})