from django.core import exceptions
from django.core.exceptions import ValidationError
import django.contrib.auth.password_validation as validators
from django.contrib.auth import get_user_model

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

import jwt
from jwt.exceptions import (
    InvalidSignatureError,
    ExpiredSignatureError,
    DecodeError
)

from decouple import config

User = get_user_model()

# Serializer for registration by getting username,password and confirmation password 
class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=250, write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "password1"]

    # Function for validating password
    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            return serializers.ValidationError(
                {"detail": "passwrods doesnt match"}
            )
        errors = dict()
        try:
            validators.validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)
        return super().validate(attrs)

    # Function for saving user without confirmation password
    def create(self, validated_data):
        validated_data.pop("password1", None)
        return User.objects.create(**validated_data)

# Serializer for creating jwt and returning jwt access,jwt refresh,username and user id 
class CustomTokenObtainSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({"username": self.user.username, "user_id": self.user.id})
        return data


# ============= Serializer for changing password of the user ============= #
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_passowrd = serializers.CharField(required=True)
    new_passowrd1 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if not user.check_password((attrs.get("old_password"))):
                raise serializers.ValidationError(
                    {"old_password": "Wrong password"}
                )
        if attrs.get("new_passowrd") != attrs.get("new_passowrd1"):
            raise serializers.ValidationError(
                {"detail": "passwords doesnt match"}
            )
        errors = dict()
        try:
            validators.validate_password(attrs.get("new_passowrd"))
        except exceptions.ValidationError as e:
            errors["new_passowrd"] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        user.set_password(attrs.get("new_passowrd"))
        user.save()
        validated_data["user"] = user
        return validated_data


class PasswordResetRequestEmailSerializer(serializers.Serializer):
    email = serializers.CharField(min_length=2,required=True)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            validated_data = super().validate(attrs)
            validated_data["user"] = user
            return validated_data
        raise serializers.ValidationError(
            {"email": "There isn't any active user with provided email address. "}
        )


class PasswordResetTokenVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=600)

    class Meta:
        model = User
        fields = ['token']

    def validate(self, attrs):
        token = attrs['token']
        try:
            payload = jwt.decode(
                token, config("SECRET_KEY"), algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
        except jwt.ExpiredSignatureError as identifier:
            return ValidationError({'detail': 'Token expired'})
        except jwt.exceptions.DecodeError as identifier:
            raise ValidationError({'detail': 'Token invalid'})

        attrs["user"] = user
        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=600)
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    password1 = serializers.CharField(
        min_length=6, max_length=68, write_only=True)

    class Meta:
        fields = ['password', 'password1', 'token']

    def validate(self, attrs):
        password = attrs.get('password')
        token = attrs.get('token')
        try:
            payload = jwt.decode(
                token, config("SECRET_KEY"), algorithms=['HS256'])
        except ExpiredSignatureError:
            raise serializers.ValidationError({
                "detail":"The token has been expired."
            })
        except InvalidSignatureError:
            raise serializers.ValidationError({
                "detail":"The token is not valid."
            })
        except DecodeError:
            raise serializers.ValidationError({
                "detail":"The token is not valid."
            })
        user = User.objects.get(id=payload['user_id'])
        if attrs["password"] != attrs["password1"]:
            raise serializers.ValidationError(
                {"details": "Passwords does not match"}
            )
        errors = dict() 
        try:
            validators.validate_password(password=attrs.get('password'))
         
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
         
        if errors:
            raise serializers.ValidationError(errors)
        user.set_password(password)
        user.save()

        return super().validate(attrs)
