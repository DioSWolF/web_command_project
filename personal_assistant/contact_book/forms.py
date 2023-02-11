from django.forms import ModelForm, CharField, TextInput, DateField
from . import models


class ContactForm(ModelForm):

    first_name = CharField(
        min_length=3, max_length=25, required=True, widget=TextInput()
    )

    last_name = CharField(min_length=3, max_length=25, required=False)
    phone = CharField(max_length=25, required=False)
    email = CharField(max_length=25, required=False)
    address = CharField(min_length=3, max_length=150, required=False)
    description = CharField(min_length=3, max_length=150, required=False)
    birthday = DateField(required=False)


    class Meta:
        model = models.ContactBook

        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "address",
            "description",
            "birthday",
        ]
        exclude = ["is_active", "change_date", "owner"]


