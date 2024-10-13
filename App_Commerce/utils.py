from django.core.mail import EmailMessage
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from . models import *
from rest_framework.exceptions import PermissionDenied


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

@handle_exceptions
def validate_category(category_id):
    try:
        category = Category.objects.get(category_id=category_id)
        return category
    except Category.DoesNotExist:
        raise PermissionDenied({"status": "failed", "message": "Category does not exist."})
    
@handle_exceptions
def validate_subcategory(subcategory_id):
    try:
        product = Subcategory.objects.get(subcategory_id=subcategory_id)
        return product
    except Subcategory.DoesNotExist:
        raise PermissionDenied({"status": "failed", "message": "Subcategory does not exist."})

@handle_exceptions
def validate_product(self, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
        return product
    except Product.DoesNotExist:
        raise PermissionDenied({"status": "failed", "message": "Product does not exist."})
    



# def handle_exception(self, exc):
    #     if isinstance(exc, PermissionDenied):
    #         return Response(exc.detail, status=status.HTTP_401_UNAUTHORIZED)
    #     return super().handle_exception(exc)