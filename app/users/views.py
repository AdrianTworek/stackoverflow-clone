from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from . import forms
from main.decorators import anonymous_required


@anonymous_required(redirect_url='main:home')
def register(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user,
                       backend='django.contrib.auth.backends.ModelBackend')
            return redirect('main:home')
    else:
        form = forms.RegisterForm()

    return render(request, 'users/register.html', {'form': form})


@anonymous_required(redirect_url='main:home')
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('main:home')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('main:users:login')
