from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
# from rest_framework_simplejwt.tokens import RefreshToken


class CustomUserManager(UserManager):
    """Custom user model manager for authentication"""

    def create(self, username, email=None, password=None, **extra_fields):
        return self.create_user(username, email, password, **extra_fields)


class CustomBaseUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, blank=True, null=True, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    picture = models.ImageField(
        upload_to="user/profile_picture/", default="user/profile_picture/default.jpeg"
    )

    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        app_label = "authentication"

    # def tokens(self):
    #     refresh = RefreshToken.for_user(self)
    #     return {
    #         "refresh": str(refresh),
    #         "access": str(refresh.access_token),
    #     }
