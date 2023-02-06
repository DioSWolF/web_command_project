from django.db import models


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=25, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Note(models.Model):
    name = models.CharField(max_length=64, null=False)
    description = models.CharField(max_length=4096, null=False)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, max_length=15)

    def __str__(self):
        return f"{self.name}"
