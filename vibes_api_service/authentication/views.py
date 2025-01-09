from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from authentication.serializers import UserSerializer, UserLoginSerializer
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from utils.security.oauth import GoogleOAuthService
from utils.email import EmailContent, EmailManager, send_email

from .models import CustomBaseUser

@api_view(['POST'])
@permission_classes([AllowAny])
def google_oauth(request):
    """
    Handle Google OAuth token verification and user creation/authentication
    """
    token = request.data.get('token')
    if not token:
        return Response(
            {'error': 'Token is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Verify Google token
    token_data = GoogleOAuthService.verify_token(token)
    if not token_data:
        return Response(
            {'error': 'Invalid token'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Get or create user
    user = GoogleOAuthService.get_or_create_user(token_data)
    if not user:
        return Response(
            {'error': 'Could not create user'},
            status=status.HTTP_400_BAD_REQUEST
        )


    return Response({
        'user': {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
    })


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = CustomBaseUser.objects.all()
    # permission_classes = [IsAuthenticated]  


    @extend_schema(
        request=UserSerializer,
        description="Add user",
        responses=UserSerializer,
        summary="Add user",
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new user profile.
        """
        user_data = request.data
        context = {"status": status.HTTP_201_CREATED, "message": "User created."}

        try:
            user = CustomBaseUser.objects.filter(
                Q(username=user_data["username"]) | Q(email=user_data["email"])
            ).first()
            # Check if user already exists and send invite message
            # if user:
            #     resend_inivite_email_if_user_exists(user.username, user.email)
            #     raise Exception("User already exists")

            serializer = self.serializer_class(data=user_data)
            if serializer.is_valid(raise_exception=True):
                new_user = serializer.create(serializer.validated_data)
                # send_account_created_email(new_user.username, new_user.email)  # Send email after user creation
            context.update({"data": serializer.data})

        except Exception as e:
            context.update(
                {
                    "message": f"{e}",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )
        return Response(data=context, status=context.pop("status"))



from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "pywebdevs@e4email.net",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()