from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    email = models.EmailField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=13, blank=True, null=True)


class EmailVerificationModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='email_verification_code')
    email_verification_code = models.CharField(max_length=4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email}, verification code: {self.email_verification_code}'

    class Meta:
        verbose_name = 'Email Verification Code'
        verbose_name_plural = 'Email Verification Codes'
        unique_together = (('user', 'email_verification_code'),)
        ordering = ['created_at']


class PhoneVerificationModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='phone_verification_code')
    phone_verification_code = models.CharField(max_length=4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.phone_number}, verification code: {self.phone_verification_code}'

    class Meta:
        verbose_name = 'Phone Verification Code'
        verbose_name_plural = 'Phone Verification Codes'
        unique_together = (('user', 'phone_verification_code'),)
        ordering = ['created_at']
