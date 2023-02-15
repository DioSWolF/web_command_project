from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=32, null=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Note(models.Model):
    name = models.CharField(max_length=64, null=False)
    description = models.CharField(max_length=4096, null=False)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, max_length=5)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def extract_tags(self):
        pass

    def __str__(self):
        return f"{self.pk}♂{self.name}♂{self.description}♂{self.tags}♂{self.created}"
