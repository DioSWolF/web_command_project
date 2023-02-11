from django.forms import ModelForm
from .models import File, Image
from django import forms



class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ["data", "name", "owner"]


class MediaForm(ModelForm):
    class Meta:
        model = File
        fields = ["data", "owner"]
