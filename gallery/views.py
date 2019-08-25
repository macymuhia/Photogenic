from django.shortcuts import render
from django.http import request
from .models import Image, Category

# Create your views here.
def index(request):
    return render(request, "index.html")


def gallery(request):
    all_cats = Category.get_all()
    return render(request, "gallery.html", {"all_cats": all_cats})


def gallery_category(request, category_id):
    pics = Image.fetch_images_in_category(category_id)
    return render(request, "category.html", {"pics": pics})

