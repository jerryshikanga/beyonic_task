from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # Urls for registration
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify/<int:telephone>/', views.VerificationPINValidationView.as_view(), name='pin_verify'),
    path('register/wait_confirmation', views.await_confirmation, name='await_confirmation'),

    # Urls for login
    path('login/success.html', views.login_success, name='login_success'),
]