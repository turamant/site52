from django.db import models

from django.conf import settings


class Crypto:
    name = models.CharField(max_length=50)
    price_usd = models.FloatField()
    price_euro = models.FloatField()
    price_gbp = models.FloatField()
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Document(models.Model):
    title = models.CharField(max_length=200)
    uploadedFile = models.FileField(upload_to="Uploaded Files/")
    dateTimeOfUpload = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
