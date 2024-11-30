from django.urls import path, include
from rest_framework.routers import DefaultRouter
from authentication.views import UserLoginViewSet, UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet)  # Register the UserViewSet

urlpatterns = [
    path("login/", UserLoginViewSet.as_view(), name="login"),
    path("auth/password_reset/", include("django_rest_passwordreset.urls", namespace="password_reset")),
] + router.urls
