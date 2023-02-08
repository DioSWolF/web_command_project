from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class ContactBook(models.Model):
    first_name = models.CharField(max_length=25, null=False)
    last_name = models.CharField(max_length=25, default=None)
    phone = PhoneNumberField(blank=True)
    email = models.EmailField(max_length=100, default=None)
    address = models.CharField(max_length=150, default=None)
    description = models.CharField(max_length=150, default=None)
    birthday = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    change_date = models.DateField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.first_name
