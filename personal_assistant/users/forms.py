from django.contrib.auth.models import User
from django.forms import (
    ModelForm,
    CharField,
    TextInput,
    PasswordInput,
    ImageField,
    FileInput,
)
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Profile


class RegisterForm(UserCreationForm):
    username = CharField(
        min_length=3, max_length=100, required=True, widget=TextInput()
    )
    password1 = CharField(max_length=50, required=True, widget=PasswordInput())
    password2 = CharField(max_length=50, required=True, widget=PasswordInput())

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar"]
