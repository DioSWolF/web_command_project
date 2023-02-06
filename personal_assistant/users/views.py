from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, decorators

from .forms import RegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm


def main(request):
    return render(request, "users/base.html")


def signup_user(request):
    if request.user.is_authenticated:
        return redirect(to="users:main")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! Your are now able to log in!')
            return redirect(to="users:login")
        else:
            return render(request, "users/register.html", context={"form": form})
    return render(request, "users/register.html", context={"form": RegisterForm()})


def login_user(request):
    if request.user.is_authenticated:
        return redirect(to="users:main")

    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"], password=request.POST["password"]
        )
        if user is None:
            messages.error(request, "Username or password didn't match")
            return redirect(to="users:login")
        login(request, user)
        messages.success(request, f'Welcome {user}!')
        return redirect(to="users:main")

    return render(request, "users/login.html", context={"form": LoginForm()})


@decorators.login_required
def logout_user(request):
    logout(request)
    return render(request, "users/logout.html")


@decorators.login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect(to="users:main")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)

