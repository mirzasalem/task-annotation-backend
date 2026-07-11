"""Custom auth helpers for SPA + cross-port dev access."""

from django.conf import settings
from rest_framework.authentication import SessionAuthentication


class DevSessionAuthentication(SessionAuthentication):
    """Skip CSRF enforcement in DEBUG so :3000 → :8000 requests work on LAN."""

    def enforce_csrf(self, request):
        if settings.DEBUG:
            return
        super().enforce_csrf(request)
