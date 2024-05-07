from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from main.decorators import anonymous_required
from questions.models import Question


@anonymous_required(redirect_url='main:home')
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user,
                       backend='django.contrib.auth.backends.ModelBackend')
            return redirect('main:home')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


@anonymous_required(redirect_url='main:home')
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('main:home')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('main:users:login')


@login_required()
def profile(request):
    return render(request, 'users/profile.html')


@login_required()
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('main:users:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'users/profile_update.html', context)


@login_required()
def user_questions(request):
    questions = Question.objects.filter(
        author=request.user).order_by('-created_at')
    questions_count = questions.count()
    return render(request, 'users/profile.html', {'questions': questions, 'questions_count': questions_count})
