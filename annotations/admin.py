from django.contrib import admin

from .models import AnnotatedImage, PolygonAnnotation

admin.site.register(AnnotatedImage)
admin.site.register(PolygonAnnotation)
