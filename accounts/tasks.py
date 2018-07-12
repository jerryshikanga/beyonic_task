from celery import task
import nexmo
from django.conf import settings
from .models import Account
import json


@task
def initiate_nexmo_verification(telephone : int, account : Account):
    client = nexmo.Client(key=settings.NEXMO_API_KEY, secret=settings.NEXMO_API_SECRET)
    account.verification_resp = client.start_verification(number=telephone, brand=settings.NEXMO_BRAND_NAME)
    account.save()


@task
def check_verification(account : Account, verification_code : str):
    json_str = account.verification_resp.replace("'", '"')
    verify_resp = json.loads(json_str)
    client = nexmo.Client(key=settings.NEXMO_API_KEY, secret=settings.NEXMO_API_SECRET)
    if "request_id" in verify_resp.keys():
        response = client.check_verification(verify_resp['request_id'], code=verification_code)
        if response['status'] == '0':
            user = account.user
            user.is_active = True
            user.save()
            return True
        else:
            return False
    else:
        return False