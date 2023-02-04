# Generated by Django 4.1.6 on 2023-02-03 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_storage', '0002_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='datatype',
            field=models.CharField(default='other', max_length=10),
        ),
        migrations.AlterField(
            model_name='file',
            name='data',
            field=models.FileField(upload_to='other/'),
        ),
    ]