from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import UserProfile


class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=False, help_text="Optional.")
    # last_name = forms.CharField(max_length=30, required=False, help_text="Optional.")
    email = forms.EmailField(
        max_length=254, help_text="Required. Inform a valid email address."
    )
    birth_date = forms.DateField(help_text="Required. Format: YYYY-MM-DD")

    class Meta:
        model = User
        fields = ("username", "email", "birth_date", "password1", "password2")


class SignInForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text="Required. Inform a valid email address."
    )
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "password")


class EditProfileForm(ModelForm):
    class Meta:
        model = User

        fields = ("email", "first_name", "last_name")


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ("city", "description", "phoneNumber", "website", "image")

