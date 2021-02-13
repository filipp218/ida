from django.db import models

# Create your models here.

class ImageMod(models.Model):
    url = models.URLField(max_length=150, blank=True)
    slug = models.SlugField(max_length=150, unique=True)
    image = models.ImageField("Изображения", blank=True)
    height = models.IntegerField("Высота", blank=True, null=True)
    width = models.IntegerField("Ширина", blank=True, null=True)
