from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first, to get the standard error response.
    response = exception_handler(exc, context)

    # Add all customized parameters to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response


class CustomException(APIException):

    # Public fields
    status_code = None
    detail = None

    # Create constructor
    def __init__(self, detail, code):
        self.detail = detail
        self.status_code = code