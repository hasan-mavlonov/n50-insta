from django.contrib import admin
from accounts.models import UserModel, EmailVerificationModel, PhoneVerificationModel

admin.site.register(UserModel)
admin.site.register(EmailVerificationModel)
admin.site.register(PhoneVerificationModel)
