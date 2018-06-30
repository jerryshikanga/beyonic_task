from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # Urls for registration
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify/<int:telephone>/', views.VerificationPINValidationView.as_view(), name='pin_verify'),
    path('register/success.html', views.register_success, name='register_success'),

    # Urls for login
    path('login/success.html', views.login_success, name='login_success'),
]