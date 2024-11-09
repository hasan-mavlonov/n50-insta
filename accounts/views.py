import threading

from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import UserModel
from accounts.serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, ResendCodeSerializer
from accounts.signals import send_verification_email


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = UserModel.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.is_active = False
        user.save()
        return user


class EmailConfirmationView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmailVerificationSerializer

    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        user = validated_data.get('user')
        email_verification_code = validated_data.get('email_verification_code_instance')

        if user and email_verification_code:
            user.is_active = True
            user.save()
            email_verification_code.delete()

            response = {
                'success': True,
                'message': "Email verified successfully!"
            }
            return Response(response, status=status.HTTP_200_OK)

        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        refresh = RefreshToken.for_user(user=serializer.validated_data['user'])
        response = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }
        return Response(response, status=status.HTTP_200_OK)


class ResendEmailVerificationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResendCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email_thread = threading.Thread(target=send_verification_email, args=('email',))
        send_verification_email(email=serializer.validated_data['email'])
        response = {
            'success': True,
            'message': "New code has been sent to your mail"
        }
        return Response(response, status=status.HTTP_200_OK)