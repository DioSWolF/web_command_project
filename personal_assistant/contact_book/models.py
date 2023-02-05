from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class ContactBook(models.Model):
    first_name = models.CharField(max_length=25, null=False)
    last_name = models.CharField(max_length=25)
    phone = models.CharField(max_length=25)
    email = models.CharField(max_length=25)
    address = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    birthday = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    change_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.first_name

