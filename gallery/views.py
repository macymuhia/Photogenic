from django.contrib.sites.models import Site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import request
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from .models import Image, Category, Location
from .forms import SignUpForm
from .tokens import account_activation_token
from .email import send_welcome_email

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
            user = form.save(commit=False)
            user.is_active = False
            # user.refresh_from_db()  # load the profile instance created by the signal
            # user.profile.birth_date = form.cleaned_data.get("birth_date")
            user.save()
            subject = "Activate Your Photopedia Account"
            current_site = Site.objects.get_current()
            print(current_site.domain)
            # current_site = get_current_site(request)
            sender = "atst.acc19@gmail.com"

            # passing in the context vairables
            text_content = render_to_string(
                "account_activation_email.txt",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            html_content = render_to_string(
                "account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )

            msg = EmailMultiAlternatives(subject, text_content, sender, [user.email])
            msg.attach_alternative(html_content, "text/html")
            res = msg.send()
            print(res)
            # send_welcome_email(user.username, user.email)
            return redirect("account_activation_sent")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def account_activation_sent(request):
    return render(request, "account_activation_sent.html")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)

        return redirect("gallery")
    else:
        return render(request, "account_activation_invalid.html")

