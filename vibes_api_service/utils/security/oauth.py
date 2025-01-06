from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from authentication.models import Profile

class GoogleOAuthService:
    @staticmethod
    def verify_token(token):
        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
            )

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Invalid issuer')

            return idinfo
        except ValueError:
            return None

    @classmethod
    def get_or_create_user(cls, token_data):
        email = token_data.get('email')
        if not email:
            return None

        user, created = Profile.objects.get_or_create(
            email=email,
            defaults={
                'username': email,
                'first_name': token_data.get('given_name', ''),
                'last_name': token_data.get('family_name', ''),
                'is_active': True
            }
        )

        if created:
            Profile.objects.create(
                user=user,
                email_verified=token_data.get('email_verified', False),
                avatar_url=token_data.get('picture'),
                provider='google'
            )

        return user