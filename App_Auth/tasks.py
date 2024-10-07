from __future__ import absolute_import, unicode_literals
from celery import shared_task
from . utils import *

@shared_task
def add(x, y):
    return x + y

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



@shared_task
def bidding_email(user, auction):
    email_body = f"""Hello {user.first_name},\n\nYou've enter a raffle draw for {auction.name}. The raffle draw will take place on {auction.start_date, auction.start_time}\n\n
Thank you for choosing Ajiroba"""
    data = {
        'email_body': email_body, 
        'to_email': user.email, 
        'email_subject': 'Ajiroba Raffle Draws!'
    }
    util.send_email(data)


@shared_task
def product_order_email(user, order):
    email_body = f"""Hello {user.first_name},\n\nYou've order successfully  and your order ID is {order.order_id}. Total cost is ₦{order.total_price}\n\n
Thank you for choosing Ajiroba"""
    data = {
        'email_body': email_body, 
        'to_email': user.email, 
        'email_subject': f'Your order is on the way {order.order_id}! - Ajiroba'
    }
    util.send_email(data)