from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserForm, CourseForm,LoginForm , RegistrationForm
from .models import User, Course
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash





def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

@login_required
def account(request):
    return render(request, 'account.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('/success/')  # Redirect to home page if user is already logged in
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user( username=username, password=password)
            return redirect('/login/')  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/registration/')  # Redirect to home page or any other authenticated page
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logoutuser(request):
    logout(request)
    return redirect('/login/')# Redirect to home or any other page

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update the session with the user's new password
            return redirect('home')  # Redirect to home page or any other page after password change
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'changepassword.html', {'form': form})




def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # Redirect to users list page or any other page
    else:
        form = UserForm()
    
    return render(request, 'create_user.html', {'form': form})

def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # Redirect to courses list page or any other page
    else:
        form = CourseForm()
    
    return render(request, 'create_course.html', {'form': form})

def users_list(request):
    users = User.objects.all()
    return render(request, 'account.html', {'users': users})

def courses_list(request):
    courses = Course.objects.all()
    return render(request, 'account.html', {'courses': courses})


def success(request):
    return render(request, 'success.html')