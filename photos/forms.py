from django.forms import ModelForm
from photos.models import ImageMod
from django.core.exceptions import ValidationError

class ImageForm(ModelForm):
    class Meta:
        model = ImageMod
        exclude = ['slug']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('url') and cleaned_data.get('image'):
            raise ValidationError(
                    "Пожалуйста, выберите только один вариант(ссылку или файл)"
                )
        if not cleaned_data.get('url') and not cleaned_data.get('image'):
            raise ValidationError(
                    "Пожалуйста, выберите хотя бы один вариант"
                )
