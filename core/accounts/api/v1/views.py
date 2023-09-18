from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from rest_framework import mixins
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from mail_templated import EmailMessage

from ..utils import EmailThread
from .serializers import (
    RegistrationSerializer,
    CustomTokenObtainSerializer,
    PasswordResetRequestEmailSerializer,
    ChangePasswordSerializer,
    SetNewPasswordSerializer,
    PasswordResetTokenVerificationSerializer,
)

User = get_user_model()  # User model


# This class used for registrating and there is a signal for creating token just after registration
class RegistrationGenericApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serialzier = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serialzier.is_valid(raise_exception=True)
        serialzier.save()
        username = serialzier.validated_data["username"]
        return Response(
            {"username": username}, status=status.HTTP_201_CREATED
        )

    @receiver(post_save, sender=User)
    def create_auth_token(sender, instance, created, **kwargs):
        if created:
            Token.objects.create(user=instance)


# This class used for loging in with auth-token by creating it
class CustomLoginToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "username": user.username,
            }
        )


# This class used for loging out by destroying auth-token
class CustomLogoutToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Customizing TokenObtainPairView
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer

# Changing password when user is authenticated 
class ChangePasswordGenericApiView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    model = get_user_model()
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user.save()
        return Response(
            {"detail": "Password updated successfully"},
            status=status.HTTP_200_OK,
        )


class PasswordResetRequestEmailGenericApiView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(
            request=request).domain
        relative_link = "/accounts/reset-password"
        absurl = 'http://'+current_site+relative_link+"/?token="+str(token)
        message = EmailMessage(
            "email/reset-password.tpl",
            {
            "user": user.username,
            "token": token,
            "link":absurl,
            "site":current_site,
            },
            "mrrahbarnia@gmail.com",
            to=[user.email],
        )
        EmailThread(message).start()
        return Response(
            {"detail": "The verification email sent to {}".format(user.email)},status=status.HTTP_200_OK
        )


class PasswordResetTokenValidateGenericApiView(mixins.RetrieveModelMixin,generics.GenericAPIView):
    serializer_class = PasswordResetTokenVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"detail":"Token is valid"},status=status.HTTP_200_OK)


class PasswordResetSetNewGenericApiView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'detail': 'Password reset successfully'}, status=status.HTTP_200_OK)
