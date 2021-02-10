from django.forms import ModelForm
from photos.models import ImageMod


class ImageForm(ModelForm):
    class Meta:
        model = ImageMod
        fields = ['image']
