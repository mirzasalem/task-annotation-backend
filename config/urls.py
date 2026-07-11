from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/tasks/", include("tasks.urls")),
    path("api/annotations/", include("annotations.urls")),
]

# Serve uploads in production too (needed on PythonAnywhere if /media/ static map is missing).
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
