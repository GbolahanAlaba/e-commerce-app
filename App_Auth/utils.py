from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage


class util:
    staticmethod
    email = EmailMessage
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()


