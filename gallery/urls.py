from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("gallery/", views.gallery, name="gallery"),
    re_path(
        r"^gallery/category/(?P<category_id>\d+)/$",
        views.gallery_category,
        name="gallery_category",
    ),
    re_path(
        r"^gallery/location/(?P<location_id>\d+)/$",
        views.pic_location,
        name="pic_location",
    ),
    path("search/", views.search_category, name="search_results"),
    path("signup", views.signup, name="signup"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

