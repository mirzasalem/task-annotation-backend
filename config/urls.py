from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/tasks/", include("tasks.urls")),
    path("api/annotations/", include("annotations.urls")),
    # Always serve uploads (Django's static() helper is a no-op when DEBUG=False).
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]
