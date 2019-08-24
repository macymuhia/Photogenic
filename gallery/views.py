from django.shortcuts import render
from django.http import request
from .models import Image

# Create your views here.
def index(request):
    return render(request, "index.html")


def gallery(request):
    pics = Image.all_images()
    return render(request, "gallery.html", {"pics": pics})

