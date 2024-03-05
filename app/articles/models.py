from django.db import models
from django.utils import timezone
from .utils import icon_image_upload

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    source = models.URLField(max_length=200, blank=True, null=True)  # Assuming source is a URL
    image = models.ImageField(upload_to=icon_image_upload, blank=True, null=True)

    create_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
