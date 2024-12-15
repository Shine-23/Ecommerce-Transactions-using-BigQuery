import logging

logger = logging.getLogger(__name__)

class FailoverLoggingMiddleware:
    """
    Middleware to log requests served by backup services.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if "X-Forwarded-For" in request.headers:  # Check if Nginx forwarded the request
            logger.info(f"Request served by backup service: {request.path}")
        return response
