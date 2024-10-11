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

def send_otp(email):
    if email:
        key = randint(100000, 999999)
        return key
    else:
        return Response({"Error"})
    
def is_valid_email(email):
      # Define the regex pattern for email validation
      pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
      return re.match(pattern, email)

def is_valid_phone(phone):
    NIGERIAN_PHONE_REGEX = re.compile(r'^(?:\+234|0)?(?:70|80|81|90|91|70|71)\d{8}$')
    return re.match(NIGERIAN_PHONE_REGEX, phone)

def is_valid_phone_w(phone):
    WORLDWIDE_PHONE_REGEX = re.compile(r'^\+(?:[0-9] ?){6,14}[0-9]$')
    return re.match(WORLDWIDE_PHONE_REGEX, phone)

def generate_referral_code(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))