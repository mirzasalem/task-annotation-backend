from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AnnotatedImageViewSet, PolygonAnnotationViewSet

router = DefaultRouter()
router.register("images", AnnotatedImageViewSet, basename="annotated-image")
router.register("polygons", PolygonAnnotationViewSet, basename="polygon")

urlpatterns = [
    path("", include(router.urls)),
]
