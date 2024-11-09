import random

from accounts.models import EmailVerificationModel, PhoneVerificationModel


def get_random_email_verification_code(email):
    email_verification_code = random.randint(1000, 9999)
    if EmailVerificationModel.objects.filter(user__email=email,
                                             email_verification_code=email_verification_code).exists():
        email_verification_code = random.randint(1000, 9999)
    return email_verification_code


def get_random_phone_verification_code(phone_number):
    phone_verification_code = random.randint(1000, 9999)
    if PhoneVerificationModel.objects.filter(user__phone_number=phone_number,
                                             phone_verification_code=phone_verification_code).exists():
        phone_verification_code = random.randint(1000, 9999)
    return phone_verification_code
