from django.contrib import admin
from accounts.models import UserModel, EmailVerificationModel, PhoneVerificationModel, FollowerModel


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone_number')
    search_fields = ('id', 'username', 'email', 'phone_number')
    list_filter = ('email', 'phone_number')


@admin.register(FollowerModel)
class FollowerModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'to_user')
    search_fields = ('user', 'to_user')
    ordering = ('created_at',)


admin.site.register(EmailVerificationModel)
admin.site.register(PhoneVerificationModel)
