from django.db import models


class News(models.Model):
    name = models.CharField(max_length=2000, null=False)
    link = models.CharField(max_length=1000, null=False)
    push_time = models.TimeField(max_length=10, null=False)
    news_type = models.CharField(max_length=50, null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
