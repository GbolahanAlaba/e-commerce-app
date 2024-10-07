from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, AuthenticationFailed) and response is not None:
        if 'detail' in response.data and response.data['detail'] == 'Invalid token.':
            response.data.pop('detail')
            response.data[""] = {"status": "failed", "message": "Invalid token."}

    return response