from twilio.rest import Client
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse


class SMS_Handler:
    # account_sid = settings.TWILIO_ACCOUNT_SID
    # auth_token = settings.TWILIO_AUTH_TOKEN

    account_sid = "AC4d1217de51de42303e3b3270a9924fa2"
    auth_token = "cc0bc7303753974e102899fb57d2d168"
    client = Client(auth_token, account_sid)

    customer_whatsapp_number=None
    service=None
    owner_number=None
    def __init__(self, customer_whatsapp_number=None, service=None, owner_number=None):
        self.customer_whatsapp_number = customer_whatsapp_number
        self.service = service
        self.owner_number = owner_number

    def send_message(self):
        if self.service:
            message_body = f'Your Service: "{self.service.sub_service}"  has been Booked Successfully',
        else:
            message_body = f'Your Service from ClickFix has been Booked Successfully',

        message = self.client.messages.create(
            from_=f'whatsapp:+91{self.owner_number}',
            body=message_body,
            to=f'whatsapp:+91{self.customer_whatsapp_number}'
        )


class Email_Handler:
    customer_email = None
    full_name = None
    def __init__(self, customer_email, full_name) -> None:
        self.customer_email = customer_email
        self.full_name = full_name

    def send_mail(self):
        subject = "ClickFix"
        if self.full_name:
            message = f"Thank You! {self.full_name} for booking your service through ClickFix! Our agent will contact you shortly."
        else:
            message = "Thank You for booking your service through ClickFix! Our agent will contact you shortly."

        from_email = settings.EMAIL_HOST_USER
        recipient_list = [self.customer_email,]
        send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)

