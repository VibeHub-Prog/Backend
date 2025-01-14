from .models import CustomBaseUser
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomBaseUser
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = CustomBaseUser.objects.create_user(**validated_data)
        return user

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

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=255)
    password = serializers.CharField(write_only=True, required=True, max_length=255)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Try to authenticate the user
        user = authenticate(username=username, password=password)
        
        if user is None:
            raise serializers.ValidationError("Invalid credentials.")
        
        data['user'] = user
        return data