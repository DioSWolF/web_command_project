# Generated by Django 4.1.6 on 2023-02-07 18:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='unknown image', max_length=100)),
                ('data', models.ImageField(upload_to='images/')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ImageStore',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.FileField(upload_to='files/')),
                ('name', models.CharField(default='New file', max_length=100)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('datatype', models.CharField(default='other', max_length=10)),
                ('in_folder', models.CharField(default='other', max_length=20)),
                ('in_trash', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'MediaStore',
            },
        ),
    ]