from django.shortcuts import render, redirect
from django.http import request
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Image, Category, Location
from .forms import SignUpForm

# import pyperclip

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
    icon = Image.icon
    # copy = pyperclip.copy(request.GET.get("copy"))
    cat_name = Image.category
    return render(
        request, "category.html", {"pics": pics, "icon": icon, "cat_name": cat_name}
    )


def pic_location(request, location_id):
    all_locations = Location.get_all()
    loc_name = Image.location

    if location_id == 00:
        pics = Image.all_images()
    else:
        pics = Image.filter_by_location(location_id)
    return render(
        request,
        "location.html",
        {"pics": pics, "all_locations": all_locations, "loc_name": loc_name},
    )


def search_category(request):

    if "category" in request.GET and request.GET["category"]:
        search_term = request.GET.get("category")
        searched_categories = Image.search_by_category(search_term)
        message = f"{search_term}"

        return render(
            request, "search.html", {"message": message, "pics": searched_categories}
        )

    else:
        message = "You haven't searched for any category"
        return render(request, "category.html", {"message": message})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("gallery")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})

