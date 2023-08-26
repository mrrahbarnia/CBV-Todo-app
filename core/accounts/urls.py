from django.urls import path
from .views import LoginView,SignUpView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

app_name = "accounts" # For dynamic url

urlpatterns = [
    # ============= This url used for login ============= #
    path("login/", LoginView.as_view(),name="login"),
    # ============= This url used for logout ============= #
    path("logout/", LogoutView.as_view(next_page=reverse_lazy("accounts:login")),name="logout"),
    # ============= This url used for signup ============= #
    path("signup/", SignUpView.as_view(),name="signup"),
]