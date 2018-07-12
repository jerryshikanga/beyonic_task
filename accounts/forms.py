from django import forms
import nexmo
from django.conf import settings
from django.contrib.auth.models import User
from .models import Account
import json


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField()
    telephone = forms.CharField(max_length =999)
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput, help_text=_("Enter the same password as above, for verification."))

    def clean_password2(self):
        def clean_password2(self):
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError( "The two password fields didn't match.", code='password_mismatch',)
            return password2

    def save(self):
        form_data = self.data
        user = User.objects.create(
            email= form_data.get("email"),
            first_name= form_data.get("first_name"),
            last_name= form_data.get("last_name"),
            username= form_data.get("email")
        )
        user.set_password(form_data.get("password"))
        user.save()

        client = nexmo.Client(key=settings.NEXMO_API_KEY, secret=settings.NEXMO_API_SECRET)
        verify_resp = client.start_verification(number=self.data['telephone'], brand=settings.NEXMO_BRAND_NAME)

        account = Account.objects.create(
            user=user,
            telephone=form_data.get("telephone"),
            verification_resp=json.dumps(verify_resp),
        )

        account.save()

        return account


class VerificationCodeValidationForm(forms.Form):
    verification_code = forms.CharField(max_length=20)

    def check_verification(self, verify_resp):
        client = nexmo.Client(key=settings.NEXMO_API_KEY, secret=settings.NEXMO_API_SECRET)
        if "request_id" in verify_resp.keys():
            response = client.check_verification(verify_resp['request_id'], code=self.data['verification_code'])
            if response['status'] == '0':
                return True
            else:
                return False
        else:
            return False
