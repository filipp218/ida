from django.urls import path
from . import views

urlpatterns = [
    path("", views.AllImages.as_view()),
    path("<slug:slug>/", views.GetImage.as_view()),
    path("add", views.Image.as_view()),
    path("<slug:slug>/cut", views.CutImage.as_view()),
]
