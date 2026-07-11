"""Dev middleware to allow API calls from frontend on a different port/host."""

from django.conf import settings


class DisableCSRFForAPIMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG and request.path.startswith("/api/"):
            request._dont_enforce_csrf_checks = True
        return self.get_response(request)
