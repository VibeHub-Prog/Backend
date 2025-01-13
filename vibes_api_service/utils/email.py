import datetime
from typing import Any, List, Optional

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from pydantic import BaseModel, EmailStr


class EmailContent(BaseModel):
    present_date: datetime.date = datetime.date.today()
    title: str
    recipients: List[EmailStr]
    subject: str
    username: str
    email: Optional[EmailStr]
    body: str
    has_action: bool
    action_name: Optional[str] = ""
    action_link: Optional[str] = ""
    action_confirm: Optional[str] = ""
    action_decline: Optional[str] = ""
    attachments: Optional[List[Any]] = []
    email_template: Optional[str] = settings.EMAIL_TEMPLATE


def send_email(content: EmailContent):
    """
    Sends an email using the specified EmailContent details.
    """
    subject = content.subject
    html_message = render_to_string(content.email_template, dict(content))
    plain_message = strip_tags(html_message)
    from_email = f"Carekojo Team <{settings.EMAIL_HOST_USER}>"
    to = content.recipients

    email = EmailMultiAlternatives(
        subject,
        plain_message,
        from_email,
        to,
    )
    email.attach_alternative(html_message, "text/html")
    for attachment in content.attachments:
        email.attach_file(attachment)
    email.send()


class EmailManager:
    """
    Service class for handling email notifications in the Carekojo platform.
    """

    def send_email_to_verify_user(self, username: str, email: str, token: str):
        """
        Sends an email to verify a user's account.
        """
        try:
            base_url = settings.BASE_URL
            content = EmailContent(
                title="Activate Account on Carekojo",
                recipients=[email],
                username=username,
                subject="Activate Your Carekojo Account",
                email=email,
                body=(
                    "To complete your account registration on Carekojo, "
                    "please click the button below to activate your account."
                ),
                has_action=True,
                action_name="Activate Account",
                action_link=f"{base_url}/patient_profile/verify/?token={token}",
                email_template=settings.EMAIL_TEMPLATE,
            )
            send_email(content)
        except Exception as e:
            print(f"Error sending verification email to user: {e}")

    def send_email_to_verify_facility(self, username: str, email: str, token: str):
        """
        Sends an email to verify a medical facility's account.
        """
        try:
            base_url = settings.BASE_URL
            content = EmailContent(
                title="Activate Account on Carekojo",
                recipients=[email],
                username=username,
                subject="Activate Your Carekojo Facility Account",
                email=email,
                body=(
                    "To complete your account registration on Carekojo, "
                    "please click the button below to activate your account."
                ),
                has_action=True,
                action_name="Activate Account",
                action_link=f"{base_url}/medical_facility/verify/?token={token}",
                email_template=settings.EMAIL_TEMPLATE,
            )
            send_email(content)
        except Exception as e:
            print(f"Error sending verification email to facility: {e}")

    def send_notification_to_user(self, recipient_email: str, subject: str, message: str, username: str):
        """
        Sends a general notification email to a user.
        """
        try:
            content = EmailContent(
                title="Notification from Carekojo",
                recipients=[recipient_email],
                username=username,
                subject=subject,
                email=recipient_email,
                body=message,
                has_action=False,
                email_template=settings.EMAIL_TEMPLATE,
            )
            send_email(content)
        except Exception as e:
            print(f"Error sending notification email to user: {e}")
