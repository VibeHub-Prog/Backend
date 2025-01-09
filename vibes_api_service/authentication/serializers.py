from .models import CustomBaseUser
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomBaseUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "picture",
        )
