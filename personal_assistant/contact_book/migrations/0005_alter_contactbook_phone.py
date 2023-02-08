# Generated by Django 4.1.4 on 2023-02-08 16:49

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("contact_book", "0004_alter_contactbook_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contactbook",
            name="phone",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=128, region=None
            ),
        ),
    ]
