from django.forms import ModelForm
from .models import File, ProfileData


class MediaForm(ModelForm):
    class Meta:
        model = File
        fields = ["data", "owner"]


class FilterForm(ModelForm):
    class Meta:
        model = ProfileData
        fields = ["filter_by", "reversed_sort"]
