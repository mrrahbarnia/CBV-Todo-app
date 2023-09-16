from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

user = get_user_model()


# This class defines login form fields and their attributes
class LoginViewForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        max_length=100,
        min_length=8,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your username here"}
        ),
    )
    password = forms.CharField(
        label="Password",
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter your password here"}
        ),
    )

    class Meta:
        model = user
        fields = ["username", "password"]


# This class defines signup form fields and their attributes
class SignUpViewForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        max_length=100,
        min_length=8,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your username here"}
        ),
    )
    password1 = forms.CharField(
        label="Password",
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter your password here"}
        ),
    )
    password2 = forms.CharField(
        label="Password",
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter the confirmation password here"}
        ),
    )

    class Meta:
        model = user
        fields = ["username", "password1", "password2"]
