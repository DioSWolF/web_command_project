from django.forms import ModelForm
from .models import File, Image, ProfileData
from django import forms



class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ["data", "name", "owner"]


class MediaForm(ModelForm):
    class Meta:
        model = File
        fields = ["data", "owner"]


class FilterForm(ModelForm):
    class Meta:
        model = ProfileData
        fields = ["filter_by", "reversed_sort"]
