from django.conf import settings
from rest_framework.authentication import SessionAuthentication


class DevSessionAuthentication(SessionAuthentication):
    # In DEBUG, skip CSRF so the Next.js app on another port can call the API.
    def enforce_csrf(self, request):
        if settings.DEBUG:
            return
        super().enforce_csrf(request)
