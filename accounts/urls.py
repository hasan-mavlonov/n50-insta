from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('all/', views.AllAccountsView.as_view(), name='all'),
    path('verify/email/', views.EmailConfirmationView.as_view(), name='verify_email'),
    path('verify/email/resend', views.ResendEmailVerificationView.as_view(), name='resend_email'),
    path('verify/phone/', views.PhoneConfirmationView.as_view(), name='verify_phone'),
    path('verify/phone/resend', views.ResendPhoneVerificationView.as_view(), name='resend_phone'),
]
