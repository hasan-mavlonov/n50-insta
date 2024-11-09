from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from accounts.models import UserModel, EmailVerificationModel, PhoneVerificationModel


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, max_length=120)
    phone_number = serializers.CharField(max_length=120, required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = UserModel
        fields = ['id', 'first_name', 'last_name', 'username', 'phone_number', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'write_only': False},
            'last_name': {'write_only': False},
        }

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return UserModel.objects.create_user(**validated_data)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        phone_number = attrs.get('phone_number')
        email = attrs.get('email')
        if password != confirm_password:
            raise serializers.ValidationError('Passwords must match')
        try:
            validate_password(password=password)
        except ValidationError as e:
            raise serializers.ValidationError(e)

        if not phone_number and not email:
            raise serializers.ValidationError('Please enter your phone number or email address')

        return attrs

    def validate_email(self, email):
        if not email.endswith('@gmail.com') or '@' not in email:
            raise serializers.ValidationError('Gmail is not correct')
        return email

    def validate_phone_number(self, phone_number):
        if not phone_number.startswith('+998'):
            raise serializers.ValidationError('Phone number should start with +998')
        return phone_number


class EmailVerificationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    email_verification_code = serializers.CharField(max_length=4)

    class Meta:
        model = EmailVerificationModel
        fields = ['email', 'email_verification_code']

    def validate(self, attrs):
        try:
            user = UserModel.objects.get(email=attrs.get('email'))
        except UserModel.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist.')
        try:
            email_verification_code = EmailVerificationModel.objects.get(
                user=user, email_verification_code=attrs['email_verification_code']
            )
        except EmailVerificationModel.DoesNotExist:
            raise serializers.ValidationError('Email verification code does not exist or is incorrect.')

        # Check if created_at is None or expired
        current_time = timezone.now()
        if email_verification_code.created_at is None:
            raise serializers.ValidationError('Verification code timestamp is missing.')

        if email_verification_code.created_at + timedelta(minutes=2) < current_time:
            # Optionally, delete expired codes
            email_verification_code.delete()
            raise serializers.ValidationError('Email verification code has expired.')

        # Add user and email_verification_code_instance to attrs so they can be used in the view
        attrs['user'] = user
        attrs['email_verification_code_instance'] = email_verification_code
        return attrs


class PhoneVerificationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    code = serializers.CharField(max_length=4)

    def validate(self, attrs):
        try:
            user_phone_code = PhoneVerificationModel(phone_number=attrs['phone_number'],
                                                     code=attrs['phone_verification_code'])
        except PhoneVerificationModel.DoesNotExist:
            raise serializers.ValidationError('Phone verification code does not exist')

        current_time = timezone.now()
        if user_phone_code.created_at + timedelta(minutes=2) < current_time:
            user_phone_code.delete()
            raise serializers.ValidationError('Phone verification code has expired')
        return attrs


class LoginSerializer(serializers.Serializer):
    email_phone_or_username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)
    error_message = "Invalid Credentials"

    def validate(self, attrs):
        email_phone_or_username = attrs.get('email_phone_or_username')
        password = attrs.get('password')
        try:
            if email_phone_or_username.endswith('@gmail.com') or '@' in email_phone_or_username:
                user = UserModel.objects.get(email=email_phone_or_username)
            elif email_phone_or_username.startswith('+998'):
                user = UserModel.objects.get(phone_number=email_phone_or_username)
            else:
                user = UserModel.objects.get(username=email_phone_or_username)

        except UserModel.DoesNotExist:
            raise serializers.ValidationError(self.error_message)
        authenticated_user = authenticate(username=user.username, password=password)
        if not authenticated_user:
            raise serializers.ValidationError(self.error_message)
        attrs['user'] = authenticated_user
        return attrs


class ResendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist.')
        email_verification_code = EmailVerificationModel.objects.get(user=user, email_verification_code=attrs[
            'email_verification_code'])
        if email_verification_code:
            current_time = timezone.now()
            if email_verification_code.created_at + timedelta(minutes=2) > current_time:
                raise serializers.ValidationError('The verification code was sent to your mail.')
        attrs['user'] = user
        return attrs