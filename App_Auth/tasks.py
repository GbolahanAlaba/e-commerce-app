from __future__ import absolute_import, unicode_literals
from celery import shared_task
from . utils import *


@shared_task
def send_activation_email(user, otp):
    email_body = f"""Hello {user.first_name},\n\nTo activate your account, please use the following One-Time Password (OTP): {otp}\n\n
Thank you for choosing Ajiroba"""
    data = {
        'email_body': email_body, 
        'to_email': user.email, 
        'email_subject': 
        'Activate Your Account with your 6 digits OTP! - Ajiroba'
    }
    util.send_email(data)

@shared_task
def verified_account_email(user):
    email_body = f"""Hello {user.first_name}, \n\nYour account is verified and activated successfully, proceed to login\n\n
Thank you for choosing Ajiroba"""
    data = {
        'email_body': email_body, 
        'to_email': user.email, 
        'email_subject': 'Congratulations! Your account is activated! - Ajiroba'
    }
    util.send_email(data)

@shared_task
def forgot_password_email(user, otp):
    email_body = f"""Hello {user.first_name},\n\nTo reset your password, please use the following One-Time Password (OTP):{otp}\n\n
Thank you for choosing Ajiroba"""
    data = {
        'email_body': email_body, 
        'to_email': user.email, 
        'email_subject': 'Reset your password with your 6 digits OTP!'
    }
    util.send_email(data)

