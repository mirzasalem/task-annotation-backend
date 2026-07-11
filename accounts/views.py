from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def csrf_token_view(request):
    return Response({"csrfToken": get_token(request)})


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get("email", "").strip().lower()
    password = request.data.get("password", "")

    if not email or not password:
        return Response(
            {"error": "Email and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    from django.contrib.auth.models import User

    try:
        user = User.objects.get(email=email)
        username = user.username
    except User.DoesNotExist:
        return Response(
            {"error": "Invalid email or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response(
            {"error": "Invalid email or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    login(request, user)
    return Response(
        {
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
            }
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"message": "Logged out successfully."})


@api_view(["GET"])
@permission_classes([AllowAny])
def me_view(request):
    if not request.user.is_authenticated:
        return Response(
            {"error": "Not authenticated."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    user = request.user
    return Response(
        {
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
            }
        }
    )
