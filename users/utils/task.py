from celery import shared_task
from django.core.mail import send_mail
from TaskMailer import settings
from users.models import ScheduledEmail




@shared_task
def send_scheduled_email(email_id):

    email = ScheduledEmail.objects.get(id=email_id)
    recipient_list = email.recipients.split(',')
    print("Sending email to:", recipient_list)


    send_mail(
        subject=email.subject,
        message=email.body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False,
    )

    email.sent = True
    email.save()
