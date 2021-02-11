import PIL.Image
from django.shortcuts import render, redirect
from django.views.generic.base import View
from photos.models import ImageMod
from photos.forms import ImageForm
from datetime import datetime
# Create your views here.

def sluggen(text):
    slug = ''
    for i in str(text):
        if i == '.':
            print(slug)
            return slug
        slug += str(i)

class Image(View):
    """Одно полное объявление"""
    def get(self, request):
        form = ImageForm()
        return render(request, "photos/image.html" , {"form": form})


    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.url = sluggen(photo.image)
            im = PIL.Image.open(photo.image)
            photo.width,photo.height = im.size
            photo.save()
            url = str(photo.url) + "/cut"
            return redirect(url)


class AllImages(View):
    """Все объявление"""
    def get(self, request):
        photos = ImageMod.objects.all()  # TODO: use custom manager
        return render(request, "photos/main.html" , {"photos": photos})

class GetImage(View):
    """Одно полное объявление"""
    def get(self, request, slug):
        photos = ImageMod.objects.get(url=slug)
        return render(request, "photos/get-image.html" , {"photos": photos})

class CutImage(View):
    def get(self, request, slug):
        photo = ImageMod.objects.get(url=slug)
        return render(request, "photos/cut.html" , {"photo": photo})

    def post(self, request, slug):
        photo = ImageMod.objects.get(url=slug)
        width = request.POST['width']
        height = request.POST['height']
        if width:
            photo.width = int(width)
        if height:
            photo.height = int(height)
        size = photo.width,photo.height
        saved = 'cut'+str(photo.image)
        img = PIL.Image.open(photo.image)
        img.thumbnail(size)
        img.save('media/' + saved)
        photo.image = saved
        photo.save()
        return redirect('/')
