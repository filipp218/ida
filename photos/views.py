from django.shortcuts import render
from photos.models import ImageMod
from photos.forms import ImageForm
# Create your views here.

class Image(View):
    """Одно полное объявление"""
    def get(self, request):
        photos = ImageMod.objects.get(url = slug)  # TODO: use custom manager
        return render(request, "photos/image.html" , {"photos": photos})


    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'photos/cut.html',)

    def put(self, request):
        pass


class AllImages(View):
    """Одно полное объявление"""
    def get(self, request):
        photos = ImageMod.objects.all()  # TODO: use custom manager
        return render(request, "photos/main.html" , {"photos": photos})
