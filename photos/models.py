from django.db import models

# Create your models here.

class ImageMod(models.Model):
    url = models.SlugField(max_length=150, unique=True)
    image = models.ImageField("Изображения", upload_to = "images",  blank=False)
