from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
import requests


# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("rate")
        else:
            messages.success(request, "Wrong credentials, try again")
            return redirect("login")
    else:
        return render(request, 'auth/login.html', {})


def logout_user(request):
    logout(request)
    return redirect("login")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            if not requests.get("https://codeforces.com/api/user.info?handles=" + form.cleaned_data['username']).ok:
                messages.error(request, f"Codeforces user named {form.cleaned_data['username']} does not exist")
                return redirect("register")
            user = form.save()
            Profile.objects.create(user=user)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful")
            return redirect('rate')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {"form": form})
