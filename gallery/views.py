from django.shortcuts import render
from django.http import request
from .models import Image, Category, Location

# Create your views here.
def index(request):
    return render(request, "index.html")


def gallery(request):
    all_cats = Category.get_all()
    all_locations = Location.get_all()
    return render(
        request, "gallery.html", {"all_cats": all_cats, "all_locations": all_locations}
    )


def gallery_category(request, category_id):
    pics = Image.fetch_images_in_category(category_id)
    return render(request, "category.html", {"pics": pics})


def pic_location(request, location_id):
    if location_id == 00:
        pics = Image.all_images()
    else:
        pics = Image.filter_by_location(location_id)
    return render(request, "location.html", {"pics": pics})

