import random

from accounts.models import EmailVerificationModel, UserModel


def get_random_email_verification_code(email):
    email_verification_code = random.randint(1000, 9999)
    if EmailVerificationModel.objects.filter(user__email=email, email_verification_code=email_verification_code).exists():
        email_verification_code = random.randint(1000, 9999)
    return email_verification_code
