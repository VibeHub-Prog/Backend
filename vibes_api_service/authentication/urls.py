from django.urls import path, include
from rest_framework.routers import DefaultRouter
from authentication.views import UserViewSet, google_oauth
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register("users", UserViewSet)  # Register the UserViewSet

urlpatterns = [
    # Login URL using JWT token obtain view
    path('api/login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("auth/password_reset/", include("django_rest_passwordreset.urls", namespace="password_reset")),
    path('oauth/google/', google_oauth, name='google_oauth'),
] + router.urls
