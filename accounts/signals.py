import threading

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import UserModel, EmailVerificationModel
from accounts.utils import get_random_email_verification_code
from conf import settings


def send_verification_email(email):
    try:
        email_verification_code = get_random_email_verification_code(email=email)
        EmailVerificationModel.objects.create(user=UserModel.objects.get(email=email),
                                              email_verification_code=email_verification_code)
        send_mail(
            subject='Verification email',
            message=f'Your verification code is: {email_verification_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )
    except Exception as e:
        print(e)


@receiver(post_save, sender=UserModel)
def send_confirmation_email(sender, instance=None, created=False, **kwargs):
    if created:
        email_thread = threading.Thread(target=send_verification_email, args=(instance.email,))
        email_thread.start()
