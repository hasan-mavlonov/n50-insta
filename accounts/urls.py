from django.urls import path
from accounts import views
from accounts.views import EmailConfirmationView, ResendEmailVerificationView

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('verify/email/', EmailConfirmationView.as_view(), name='verify_email'),
    path('accounts/verify/resend', ResendEmailVerificationView.as_view(), name='resend_email'),

]
