from rest_framework import serializers

from .models import AnnotatedImage, PolygonAnnotation


class PolygonAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolygonAnnotation
        fields = ["id", "points", "label", "color", "created_at"]
        read_only_fields = ["created_at"]


class AnnotatedImageSerializer(serializers.ModelSerializer):
    polygons = PolygonAnnotationSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = AnnotatedImage
        fields = ["id", "name", "image", "image_url", "polygons", "created_at"]
        read_only_fields = ["created_at", "image_url"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        if obj.image:
            return obj.image.url
        return None

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        image_file = validated_data.get("image")
        if image_file and not validated_data.get("name"):
            validated_data["name"] = image_file.name
        return super().create(validated_data)


class PolygonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolygonAnnotation
        fields = ["id", "image", "points", "label", "color"]

    def validate_image(self, value):
        user = self.context["request"].user
        if value.user != user:
            raise serializers.ValidationError("Image not found.")
        return value
