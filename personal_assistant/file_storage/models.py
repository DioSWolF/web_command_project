from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


data_types = {
    (
        "MP3",
        "OGG",
        "VORBIS",
        "FLAC",
        "WAV",
        "PCM",
        "AIFF",
        "AAC",
        "WMA",
        "FLAC",
        "ALAC",
    ): "audio",
    ("PNG", "JPG", "JPEG", "GIF", "SVG", "TIF", "TIFF", "EPS"): "image",
    (
        "MP4",
        "MOV",
        "WMV",
        "AVI",
        "AVCHD",
        "FLV",
        "F4V",
        "SWF",
        "MKV",
        "WEBM",
        "HTML5",
        "MPEG-2",
        "MPG",
        "MP2",
        "MPEG",
        "MPE",
        "MPV",
        "WMV",
        "AVCHD",
    ): "video",
    (
        "PDF",
        "DOC",
        "DOCX",
        "HTML",
        "HTM",
        "XLS",
        "XLSX",
        "TXT",
        "PPT",
        "PPTX",
        "ODP",
        "KEY",
    ): "document",
}

folders = {"image": "images",
           "audio": "audio",
           "video": "video",
           "document": "documents",
           "other": "other",
           }


class File(models.Model):
    data = models.FileField(upload_to='files/')
    name = models.CharField(max_length=100, default="New file")

    date_posted = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    datatype = models.CharField(max_length=10, default="other")
    in_folder = models.CharField(max_length=20, default="other")
    in_trash = models.BooleanField(default=False)
    size = models.IntegerField(default=0)

    class Meta:
        db_table = "MediaStore"

    def __str__(self):
        max_len = 10
        if str(self.datatype) == "audio":
            max_len = 30
        return str(self.name) if len(str(self.name)) < max_len else str(self.name)[:max_len-3]+"..."

    def size_str(self, *args, **kwargs):
        if self.size > 1024**2:
            return f"{int(self.size) // (1024**2)} MB"
        if self.size > 1024:
            return f"{int(self.size) // (1024**1)} KB"
        return f"{int(self.size)} B"

    def save(self, *args, **kwargs):
        extension = str(self.data).split(".")[-1]
        for tpl, data_type in data_types.items():

            if extension.upper() in tpl:
                self.datatype = data_type

                self.data.upload_to = f'{self.datatype}/'
                if self.in_trash:
                    self.in_folder = "trash"
                else:
                    self.in_folder = folders.get(self.datatype)
                break
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        storage = self.data.storage
        if storage.exists(self.data.name):
            storage.delete(self.data.name)
        super().delete()


class ProfileData(models.Model):
    filters = [("name", "Name"), ("date_posted", "Upload date"), ("size", "Size")]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    filter_by = models.CharField(max_length=15, choices=filters, default="name")
    reversed_sort = models.BooleanField(default=False)
    max_capacity = models.IntegerField(default=100*1024*1024)#524288000)
    memory_occupied = models.IntegerField(default=0)
    max_num_of_files = models.IntegerField(default=200)
    num_of_files = models.IntegerField(default=0)

    class Meta:
        db_table = "MediaFilter"


    class Meta:
        db_table = "ImageStore"