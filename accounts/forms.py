from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from .models import Account
import json
from .tasks import initiate_nexmo_verification
import nexmo


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField()
    telephone = forms.CharField(max_length=999)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput, help_text="Enter the same password as above, for verification.")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.", code='password_mismatch', )
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email addresses must be unique.')
        return email

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if telephone and Account.objects.filter(telephone=telephone).exists():
            raise forms.ValidationError('Telephone number must be unique.')
        return telephone

    def save(self):
        form_data = self.data
        user = User.objects.create(
            email=form_data.get("email"),
            first_name=form_data.get("first_name"),
            last_name=form_data.get("last_name"),
            username=form_data.get("email"),
            is_active=False,
        )
        user.set_password(form_data.get("password2"))
        user.save()

        account = Account.objects.create(
            user=user,
            telephone=form_data.get("telephone"),
            verification_resp=json.dumps(dict()),
        )
        account.save()

        #function changed to be called asynchronously
        # initiate_nexmo_verification(telephone=form_data.get("telephone"), account=account)
        initiate_nexmo_verification.apply_async(args=None, kwargs={"telephone": form_data.get("telephone"), "account": account})

        return account


class VerificationCodeValidationForm(forms.Form):
    verification_code = forms.CharField(max_length=20)
