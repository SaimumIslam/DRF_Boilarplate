import logging
from time import time
from rest_framework.views import exception_handler


class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        requested_at = time()
        logging.info(f"Incoming request: {request.method} {request.path}")

        response = self.get_response(request)

        response_at = time()
        executing_duration = int((response_at - requested_at) * 1000)  # second
        logging.info(f"Outgoing response: {response.status_code} {executing_duration}")

        return response
