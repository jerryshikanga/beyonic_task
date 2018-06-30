from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    verification_resp = models.TextField(blank=True, null=True)
    telephone = models.IntegerField(unique=True)

    def __str__(self):
        return self.user.get_full_name()
