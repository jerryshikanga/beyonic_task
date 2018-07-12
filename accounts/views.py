from django.views.generic import FormView
from .forms import VerificationCodeValidationForm, RegisterForm
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from .models import Account
from .tasks import check_verification
import json


# Create your views here.
class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "accounts/register.html"

    def __init__(self):
        super(RegisterView, self).__init__()
        self.account = None

    def get_success_url(self):
        return reverse_lazy("accounts:pin_verify", kwargs={
            "telephone": self.account.telephone
        })

    def form_valid(self, form):
        self.account = form.save()
        # super(RegisterView, self).form_valid(form)
        return HttpResponseRedirect(reverse_lazy("accounts:pin_verify", kwargs={
            "telephone": int(self.account.telephone)
        }))


class VerificationPINValidationView(FormView):
    form_class = VerificationCodeValidationForm
    template_name = "accounts/verification_code_form.html"
    success_url = reverse_lazy("accounts:register_success")

    def form_valid(self, form):
        account = get_object_or_404(Account, telephone=self.kwargs['telephone'])
        check_verification(account, form.data["verification_code"])
        return HttpResponseRedirect(reverse_lazy("accounts:await_confirmation"))


def await_confirmation(request):
    return render(request, "accounts/await_confirmation.html")


def login_success(request):
    return render(request, "accounts/login_success.html")