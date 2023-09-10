from django.core import exceptions
import django.contrib.auth.password_validation as validators
from django.contrib.auth import get_user_model

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

# ============= Serializer for registration by getting username,password and confirmation password ============= #
class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=250, write_only=True)
    class Meta:
        model = User
        fields = ['username','password','password1']
    # Function for validating password
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password1'):
            return serializers.ValidationError(
                {'detail':'passwrods doesnt match'}
                )
        errors = dict()
        try:
            validators.validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            errors['password']=list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)
        return super().validate(attrs)
    # Function for saving user without confirmation password
    def create(self, validated_data):
        validated_data.pop('password1',None)
        return User.objects.create(**validated_data)
    
# ============= Serializer for creating jwt and returning jwt access,jwt refresh,username and user id ============= #
class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update(
            {'username':self.user.username,'user_id':self.user.id}
            )
        return data
    
# ============= Serializer for changing password of the user ============= #
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True,write_only=True)
    new_passowrd = serializers.CharField(required=True)
    new_passowrd1 = serializers.CharField(required=True,write_only=True)
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        user = None
        request = self.context.get('request')
        if request and hasattr(request,'user'):
            user = request.user
            if not user.check_password((attrs.get('old_password'))):
                raise serializers.ValidationError({'old_password':'Wrong password'})
        if attrs.get('new_passowrd') != attrs.get('new_passowrd1'):
            raise serializers.ValidationError(
                {'detail':'passwords doesnt match'}
            )
        errors = dict()
        try:
            validators.validate_password(attrs.get('new_passowrd'))
        except exceptions.ValidationError as e:
            errors['new_passowrd']=list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        user.set_password(attrs.get('new_passowrd'))
        user.save()
        validated_data['user'] = user
        return validated_data


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            validated_data = super().validate(attrs)
            validated_data['user'] = user
            return validated_data
        raise serializers.ValidationError({'email':"There isn't any active user with this email address. "})


class PasswordResetDoneSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True,write_only=True)
    def validate(self, attrs):
        validated_data =  super().validate(attrs)
        if attrs.get('new_passowrd') != attrs.get('new_passowrd1'):
            raise serializers.ValidationError(
                {'detail':'passwords doesnt match'}
            )
        errors = dict()
        try:
            validators.validate_password(attrs.get('new_passowrd'))
        except exceptions.ValidationError as e:
            errors['new_passowrd']=list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        validated_data['new_passowrd'] = attrs.get('new_password')
        return validated_data

        

    
        
        
    