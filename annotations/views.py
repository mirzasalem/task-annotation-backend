from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .models import AnnotatedImage, PolygonAnnotation
from .serializers import (
    AnnotatedImageSerializer,
    PolygonAnnotationSerializer,
    PolygonCreateSerializer,
)


class AnnotatedImageViewSet(viewsets.ModelViewSet):
    serializer_class = AnnotatedImageSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return AnnotatedImage.objects.filter(user=self.request.user).prefetch_related(
            "polygons"
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PolygonAnnotationViewSet(viewsets.ModelViewSet):
    serializer_class = PolygonAnnotationSerializer

    def get_queryset(self):
        return PolygonAnnotation.objects.filter(
            image__user=self.request.user
        ).select_related("image")

    def get_serializer_class(self):
        if self.action == "create":
            return PolygonCreateSerializer
        return PolygonAnnotationSerializer

    @action(detail=False, methods=["post"])
    def bulk_save(self, request):
        """Replace all polygons for one image."""
        image_id = request.data.get("image_id")
        polygons_data = request.data.get("polygons", [])

        if not image_id:
            return Response(
                {"error": "image_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            image = AnnotatedImage.objects.get(id=image_id, user=request.user)
        except AnnotatedImage.DoesNotExist:
            return Response(
                {"error": "Image not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        image.polygons.all().delete()

        created = []
        for poly_data in polygons_data:
            polygon = PolygonAnnotation.objects.create(
                image=image,
                points=poly_data.get("points", []),
                label=poly_data.get("label", ""),
                color=poly_data.get("color", "#6366f1"),
            )
            created.append(polygon)

        serializer = PolygonAnnotationSerializer(created, many=True)
        return Response(serializer.data)
