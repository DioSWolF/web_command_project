from django.forms import ModelForm
from .models import File
from django import forms


class MediaForm(ModelForm):
    class Meta:
        model = File
        fields = [
            'data',
            'owner'
        ]

