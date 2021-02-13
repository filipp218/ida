import PIL.Image
import requests
from django.shortcuts import render, redirect
from django.views.generic.base import View
from photos.models import ImageMod
from photos.forms import ImageForm
from django.core.exceptions import ValidationError

def sluggen(text):
    """функция, которая генерирует slug
    для добавленных изображений исходя
    из их имени или ссылке откуда они скачаны"""
    slug = ''
    alphabet = {'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm','1','2','3','4','5','6','7','8','9','0'}
    russian = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
                'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
                'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
                'я': 'ya', ' ': '-'}
    for i in str(text):
        if i in alphabet:
            slug += str(i)
        elif i in russian:
            slug += str(russian[i])
    return slug




class Image(View):
    """Форма для добавления изображения"""
    def get(self, request):
        form = ImageForm()
        return render(request, "photos/image.html" , {"form": form})


    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        if not form.is_valid():
            e = {}
            for field in form.errors:
               e[field]=form.errors[field].as_text()
            e = e['__all__']
            return render(request, "photos/image.html" , {"form": form, "e": e})

        if form.cleaned_data.get('url'):
            url = form.cleaned_data.get('url')
            try:
                p = requests.get(url)
            except :
                return render(request, "photos/error.html")

            slug = sluggen(url)
            with open(f'media/{slug}.jpg', "wb") as out:
                out.write(p.content)
            photo = ImageMod(slug=slug, image= f'{slug}.jpg', url=url)

        elif form.cleaned_data.get('image'):
            photo = form.save(commit=False)
            photo.slug = sluggen(photo.image)

        im = PIL.Image.open(photo.image)
        photo.width,photo.height = im.size
        photo.save()
        return redirect(f'/{photo.slug}')


class AllImages(View):
    """Все изображения"""
    def get(self, request):
        e = ''
        photos = ImageMod.objects.all()
        if not photos:
            e = 'Нет доступных изображений'
        return render(request, "photos/main.html" , {"photos": photos, "e":e})

class CutImage(View):
    """Для обрезки изображения"""
    def get(self, request, slug):
        photo = ImageMod.objects.get(slug=slug)
        form = ImageForm()
        return render(request, "photos/cut.html" , {"photo": photo, "form": form})

    def post(self, request, slug):
        photo = ImageMod.objects.get(slug=slug)
        width = request.POST['width']
        height = request.POST['height']
        if width:
            photo.width = int(width)
        if height:
            photo.height = int(height)
        size = photo.width, photo.height
        name, ext = str(photo.image).rsplit('.', 1)
        saved = f'{name}.{photo.width}x{photo.height}.{ext}'
        img = PIL.Image.open(photo.image)
        img.thumbnail(size)
        img.save('media/' + saved)
        photo.image = saved
        photo.save()
        return redirect(f'/{photo.slug}')
