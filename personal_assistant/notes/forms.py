from django.forms import ModelForm, CharField
from .models import Tag, Note


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=32, required=True)

    class Meta:
        model = Tag
        fields = ['name', 'owner']


class NoteForm(ModelForm):
    name = CharField(min_length=5, max_length=64, required=True)
    description = CharField(min_length=10, max_length=4096, required=True)

    class Meta:
        model = Note
        fields = ['name', 'description', 'owner']
        exclude = ['tags']
