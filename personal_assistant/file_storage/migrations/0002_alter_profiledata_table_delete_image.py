# Generated by Django 4.1.6 on 2023-02-11 19:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("file_storage", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="profiledata",
            table="ImageStore",
        ),
        migrations.DeleteModel(
            name="Image",
        ),
    ]
