import threading

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from twilio.rest import Client

from accounts.models import UserModel, EmailVerificationModel, PhoneVerificationModel
from accounts.utils import get_random_email_verification_code, get_random_phone_verification_code
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


def send_verification_phone(phone_number):
    phone_verification_code = get_random_phone_verification_code(phone_number=phone_number)
    message_to_broadcast = f'Your verification code is: {phone_verification_code}'
    PhoneVerificationModel.objects.create(user=UserModel.objects.get(phone_number=phone_number),
                                          phone_verification_code=phone_verification_code)
    recipient_list = [phone_number]
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    for recipient in recipient_list:
        print(recipient)
        if recipient:
            client.messages.create(to=recipient,
                                   from_=settings.TWILIO_NUMBER,
                                   body=message_to_broadcast)
    return HttpResponse("messages sent!" + message_to_broadcast, 200)


@receiver(post_save, sender=UserModel)
def send_confirmation_email(sender, instance=None, created=False, **kwargs):
    if created:
        email_thread = threading.Thread(target=send_verification_email, args=(instance.email,))
        email_thread.start()


@receiver(post_save, sender=UserModel)
def send_confirmation_code(sender, instance=None, created=False, **kwargs):
    if created:
        phone_thread = threading.Thread(target=send_verification_phone, args=(instance.phone_number,))
        phone_thread.start()
