from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

import jwt
from jwt.exceptions import (
    InvalidSignatureError,
    ExpiredSignatureError
)

from mail_templated import EmailMessage
from decouple import config

from ..utils import EmailThread
from .serializers import (
<<<<<<< Updated upstream
RegistrationSerializer,CustomTokenObtainSerializer,PasswordResetSerializer,
ChangePasswordSerializer,PasswordResetDoneSerializer
=======
    RegistrationSerializer,
    CustomTokenObtainSerializer,
    PasswordResetSerializer,
    ChangePasswordSerializer,
    SetNewPasswordSerializer,
>>>>>>> Stashed changes
)

User = get_user_model() # User model

# ============= This class used for registrating and there is a signal for creating token just after registration ============= #
class RegistrationGenericApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serialzier = self.serializer_class(data=request.data,context={'request': request})
        serialzier.is_valid(raise_exception=True)
        serialzier.save()
        username = serialzier.validated_data['username']
        return Response({'username':username},status=status.HTTP_201_CREATED)
    @receiver(post_save, sender=User)
    def create_auth_token(sender, instance, created, **kwargs):
        if created:
            Token.objects.create(user=instance)
    
# ============= This class used for loging in with auth-token by creating it ============= #
class CustomLoginToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })

# ============= This class used for loging out by destroying auth-token ============= #
class CustomLogoutToken(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# ============= Customizing TokenObtainPairView ============= #
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer


class ChangePasswordGenericApiView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    model = get_user_model()
    permission_classes = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.save()
        return Response({'detail':'Password updated successfully'},status=status.HTTP_200_OK)
    

class ResetPasswordGenericApiView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    def post(self, request, *args, **kwargs):
<<<<<<< Updated upstream
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        message = EmailMessage('email/reset-password.tpl', {'user': user.username,'token':self.get_token_for_user(user)}, 'mrrahbarnia@gmail.com',
                       to=[user.email])
=======
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        current_site = get_current_site(request)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = self.get_token_for_user(user)
        relative_link = reverse('accounts:api-v1:reset-password-checktoken',kwargs={'token':token})
        message = EmailMessage(
            "email/reset-password.tpl",
            {"user": user.username,
            "token": token,
            "current_site": 'http://'+str(current_site)+str(relative_link)},
            "mrrahbarnia@gmail.com",
            to=[user.email],
        )
>>>>>>> Stashed changes
        EmailThread(message).start()
        return Response({"detail":"The verification email sent to {}".format(user.email)})
    def get_token_for_user(swlf,user):
        refresh = RefreshToken.for_user(user)
        return str(refresh)

<<<<<<< Updated upstream
class ResetPasswordConfirmationGenericApiView(generics.GenericAPIView):
    serializer_class = PasswordResetDoneSerializer
    def get_queryset(self):
        token = self.request.parser_context.get('kwargs').get('token')
        try:
            token = jwt.decode(token, config('SECRET_KEY'), algorithms=['HS256'])
        except InvalidSignatureError:
            return Response({'detail':'The token is not valid,please get a new link with {}'})
        user = User.objects.filter(id=token.get('user_id')).first()
        return user
    def get(self, request, *args, **kwargs):
        user = self.get_queryset()
        if not user:
            return Response({"detail":"There isn't any user with this token."},status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"Token is valid,Please Enter your new password."})
    def post(self, request, *args, **kwargs):
        user = self.get_queryset()
        if not user:
            return Response({"detail":"There isn't any user with this token."},status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data('new_password')
        user.set_password(new_password)
        user.save()
        return Response({"detail":"Your password reseted successfully"})
=======

class ResetPasswordCheckTokenApiView(APIView):

    def get(self, request, *args, **kwargs):
        token = self.request.parser_context.get("kwargs").get("token")
        try:
            jwt_token = jwt.decode(
                token, config("SECRET_KEY"), algorithms=["HS256"]
            )
        except InvalidSignatureError:
            return Response(
                {
                    "detail": "The token is not valid,please get a new link."
                }
            )
        except ExpiredSignatureError:
            return Response(
                {
                    "detail": "The token has been expired,please get a new link."
                }
            )
        user = User.objects.filter(id=jwt_token.get("user_id")).first()
        if not user:
            return Response(
                {"detail": "There isn't any user with this token."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"detail": "Token is valid",
             "token":token},
             status=status.HTTP_200_OK
        )


class SetNewPasswordGenericApiView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,context={'request':request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {'detail':'The password has been changed successfully'},
            status=status.HTTP_200_OK
        )

>>>>>>> Stashed changes
