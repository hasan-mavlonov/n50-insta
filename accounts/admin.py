from django.contrib import admin
from accounts.models import UserModel, EmailVerificationModel, PhoneVerificationModel


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone_number')
    search_fields = ('id', 'username', 'email', 'phone_number')
    list_filter = ('email', 'phone_number')


admin.site.register(EmailVerificationModel)
admin.site.register(PhoneVerificationModel)
