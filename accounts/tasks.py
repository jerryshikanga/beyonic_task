from celery import task
import nexmo
from django.conf import settings
from .models import Account


@task
def initiate_nexmo_verification(telephone : int, account : Account):
    client = nexmo.Client(key=settings.NEXMO_API_KEY, secret=settings.NEXMO_API_SECRET)
    account.verification_resp = client.start_verification(number=telephone, brand=settings.NEXMO_BRAND_NAME)
    account.save()