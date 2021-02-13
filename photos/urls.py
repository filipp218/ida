from django.urls import path
from . import views

urlpatterns = [
    path("", views.AllImages.as_view()),
    path("add", views.Image.as_view()),
    path("<slug:slug>", views.CutImage.as_view()),
]
