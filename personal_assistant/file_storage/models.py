from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# from PIL import Image

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
           "document": "document",
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

    class Meta:
        db_table = "MediaStore"

    def save(self, *args, **kwargs):
        # print(self.data)
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
        # print(f"filetype : {self.datatype}")
        super().save(*args, **kwargs)


class Image(models.Model):
    # data = models.FileField(upload_to='images/')
    name = models.CharField(max_length=100, default="unknown image")
    data = models.ImageField(upload_to="images/")
    date_posted = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # owner

    class Meta:
        db_table = "ImageStore"

