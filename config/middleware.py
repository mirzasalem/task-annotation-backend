from django.conf import settings


class DisableCSRFForAPIMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Local only: frontend and API run on different ports.
        if settings.DEBUG and request.path.startswith("/api/"):
            request._dont_enforce_csrf_checks = True
        return self.get_response(request)
