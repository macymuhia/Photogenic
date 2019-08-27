from django.db import models
import urllib, os
from urllib.parse import urlparse
from fontawesome.fields import IconField

# Create your models here.
class Location(models.Model):
    place = models.CharField(max_length=30)

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    def __str__(self):
        return self.place


class Category(models.Model):
    name = models.CharField(max_length=30)
    cat_image = models.ImageField(upload_to="gallery/category/", default="")
    cat_description = models.CharField(max_length=255, blank=True)

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to="gallery/")
    image_name = models.CharField(max_length=10)
    image_url = models.URLField(null=True, blank=True)
    image_description = models.CharField(max_length=30)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    category = models.ManyToManyField(Category)
    created_on = models.DateTimeField(auto_now_add=True)
    icon = IconField()

    class Meta:
        ordering = ["-created_on"]

    @classmethod
    def all_images(cls):
        pics = cls.objects.all()
        return pics

    @classmethod
    def display_category(cls, category):
        pics = cls.objects.filter(category=category)
        return pics

    @classmethod
    def fetch_images_in_category(cls, category_id):
        return cls.objects.filter(category__id=category_id)

    @classmethod
    def filter_by_location(cls, location_id):
        return cls.objects.filter(location=location_id)

    @classmethod
    def search_by_category(cls, search_term):
        return cls.objects.filter(category__name__icontains=search_term)

    @classmethod
    def save_image(cls, *args, **kwargs):
        if cls.image_url:
            file_save_dir = cls.upload_path
            filename = urlparse(cls.image_url).path.split("/")[-1]
            urllib.urlretrieve(cls.image_url, os.path.join(file_save_dir, filename))
            cls.image = os.path.join(file_save_dir, filename)
            cls.image_url = ""
        super(Image, cls).save()

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.image_url.path):
            os.remove(self.image_url.path)
        super(Image, self).delete(*args, **kwargs)

    @classmethod
    def get_image_by_id(cls, id):
        return cls.objects.filter(id=id)

    @classmethod
    def search_image(cls, category):
        return cls.objects.filter(category__name__icontains=category)

    def __str__(self):
        return self.image_name
