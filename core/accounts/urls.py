from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

from .views import LoginView, SignUpView

app_name = "accounts"  # For dynamic url

urlpatterns = [
    # This url used for login
    path("login/", LoginView.as_view(), name="login"),
    # This url used for logout
    path(
        "logout/",
        LogoutView.as_view(next_page=reverse_lazy("accounts:login")),
        name="logout",
    ),
    # This url used for signup
    path("signup/", SignUpView.as_view(), name="signup"),
    # This url includes all api v1 urls for the accounts app
    path("api/v1/", include("accounts.api.v1.urls")),
    # This url includes all api v2 urls for the accounts app
]
