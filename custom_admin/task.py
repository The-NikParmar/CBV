from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(email, password):
    subject = 'Welcome to HMS'
    message = f'''
    Hello,

    Welcome to HMS. Your account has been
    created successfully.

    Email: {email}
    Password: {password}

    Best regards,
    The HMS Team.
    '''
    
    from_email = settings.EMAIL_HOST_USER
    to_email = email

    send_mail(subject, message, from_email, [to_email])
