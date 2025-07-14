

from django.core.mail import send_mail

from TaskMailer import settings
from users.models import OTP


from datetime import datetime, timedelta
from django.utils import timezone
import random


def generate_otp(user):

    code = str(random.randint(100000, 999999))
    expires_at = timezone.now() + timedelta(minutes=5)

    OTP.objects.create(
        user=user,
        otp=code,
        expires_at=expires_at
    )

    send_mail(
        subject='Your OTP Code',
        message=f'Your OTP is {code}. It expires in 5 minutes.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email]
    )
