from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
import re
import random
import string
from random import randint


class util:
    staticmethod
    email = EmailMessage
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()



def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_message = str(e)
            return Response({"status": "failed", "message": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper
