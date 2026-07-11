from django.db import models
from django.contrib.auth.models import User


class AnnotatedImage(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="annotated_images"
    )
    image = models.ImageField(upload_to="annotations/")
    name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.name or f"Image {self.id}"


class PolygonAnnotation(models.Model):
    image = models.ForeignKey(
        AnnotatedImage, on_delete=models.CASCADE, related_name="polygons"
    )
    points = models.JSONField()
    label = models.CharField(max_length=100, blank=True, default="")
    color = models.CharField(max_length=20, default="#6366f1")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Polygon {self.id} on {self.image_id}"
