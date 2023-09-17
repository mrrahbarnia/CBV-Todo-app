from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from . import views

app_name = "api-v1"  # For dynamic url

urlpatterns = [
    # ============= Registration ============= #
    path(
        "registration/",
        views.RegistrationGenericApiView.as_view(),
        name="registration",
    ),
    # ============= AuthToken Login/Logout ============= #
    path(
        "login/token/", views.CustomLoginToken.as_view(), name="login-token"
    ),
    path(
        "logout/token/",
        views.CustomLogoutToken.as_view(),
        name="logout-token",
    ),
    # ============= JWT Create/Refresh/Verify ============= #
    path(
        "jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    # ============= Activation Confirm/Resend ============= #
    # ============= Change Password ============= #
    path(
        "change-password/",
        views.ChangePasswordGenericApiView.as_view(),
        name="change-password",
    ),
    # ============= Reset Password ============= #
    path(
        "reset-password/",
        views.ResetPasswordGenericApiView.as_view(),
        name="password_reset",
    ),
    path(
        "reset-password/<str:token>",
        views.ResetPasswordCheckTokenApiView.as_view(),
        name="password_confirm",
    )
]
