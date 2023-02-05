from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, decorators

from .forms import RegisterForm, LoginForm, ProfileForm


def main(request):
    return render(request, "users/base.html")


def signup_user(request):
    if request.user.is_authenticated:
        return redirect(to="users:main")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="users:main")
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
        return redirect(to="users:main")

    return render(request, "users/login.html", context={"form": LoginForm()})


@decorators.login_required
def logout_user(request):
    logout(request)
    return redirect(to="users:main")


@decorators.login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile is updated!")
            return redirect(to="users:profile")

    return render(
        request,
        "users/profile.html",
        context={"form": ProfileForm(instance=request.user.profile)},
    )
