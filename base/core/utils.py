from django.db import IntegrityError, DatabaseError
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .exceptions import NOTImplemented, AttributeNotFound, Conflicted, DBError


def custom_exception_handler(exception, context):
    response = exception_handler(exception, context)

    if response is None:
        """
        error not catch by django server
        """
        if isinstance(exception, NotImplementedError):
            error_response = NOTImplemented(exception)
        elif isinstance(exception, AttributeError):
            error_response = AttributeNotFound(exception)
        elif isinstance(exception, IntegrityError):
            error_response = Conflicted(exception)
        elif isinstance(exception, DatabaseError):
            error_response = DBError(exception)
        else:
            error_response = APIException(exception)
        response_data = {
            "detail": error_response.detail or error_response.default_detail,
            "file_name": context["view"].__class__.__name__
        }
        return Response(response_data, status=error_response.status_code)

    return response
