from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from accounts.models import UserModel, EmailVerificationModel, PhoneVerificationModel


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'


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
            email_verification_code = EmailVerificationModel.objects.get(
                user=user, email_verification_code=attrs['email_verification_code']
            )
        except Exception as e:
            raise serializers.ValidationError(f"Error{e}")
        current_time = timezone.now()
        if email_verification_code.created_at + timedelta(minutes=2) < current_time:
            email_verification_code.delete()
            raise serializers.ValidationError('Email verification code has expired.')
        attrs['user'] = user
        attrs['email_verification_code_instance'] = email_verification_code
        return attrs


class PhoneVerificationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    phone_verification_code = serializers.CharField(max_length=4)

    class Meta:
        model = PhoneVerificationModel
        fields = ['phone_number', 'phone_verification_code']

    def validate(self, attrs):
        try:
            user = UserModel.objects.get(phone_number=attrs.get('phone_number'))
            phone_verification_code = PhoneVerificationModel.objects.get(
                user=user, phone_verification_code=attrs['phone_verification_code']
            )
        except Exception as e:
            raise serializers.ValidationError(f"Error{e}")
        current_time = timezone.now()
        if phone_verification_code.created_at + timedelta(minutes=2) < current_time:
            phone_verification_code.delete()
            raise serializers.ValidationError('Phone verification code has expired.')
        attrs['user'] = user
        attrs['phone_verification_code_instance'] = phone_verification_code
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


class ResendEmailCodeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist.')
        attrs['user'] = user
        return attrs

    class Meta:
        model = EmailVerificationModel
        fields = ['email']


class ResendPhoneCodeSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        try:
            user = UserModel.objects.get(phone_number=phone_number)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError('User with this phone number does not exist.')
        attrs['user'] = user
        return attrs

    class Meta:
        model = PhoneVerificationModel
        fields = ['phone_number']
