from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models

# Create your models here.
from django.urls import reverse

private_storage = FileSystemStorage(location=settings.PRIVATE_STORAGE_ROOT)

class Book(models.Model):

    title = models.CharField(max_length=100, unique=True, null=False)
    author = models.CharField(max_length=100, null=False)
    genre = models.CharField(max_length=20, null=False)
    rating = models.IntegerField()
    cover = models.ImageField(null=False, default='bitcoin.png', upload_to='images/')
    upload = models.FileField(storage=private_storage, null=True)
    description = models.TextField()
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'<Book {self.title}>'

    def get_absolute_url(self):
        return reverse('reader:detail', args=[str(self.pk)])
