from django.db import models

# Create your models here.

class ImageMod(models.Model):
    url = models.SlugField(max_length=150, unique=True, blank=True)
    image = models.ImageField("Изображения", blank=True)
    height = models.IntegerField("Высота", blank=True, null=True)
    weight = models.IntegerField("Ширина", blank=True, null=True)
