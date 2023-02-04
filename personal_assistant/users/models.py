from django.contrib.auth.models import User
from django.db import models
from PIL import Image
# Create your models here.


class Profile(models.Model):
    avatar = models.ImageField(default='avatar_default.png', upload_to='profile_images')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        pic = Image.open(self.avatar.path)

        if pic.height > 225 or pic.width > 225:
            pic.thumbnail((225, 225))
            pic.save(self.avatar.path)
