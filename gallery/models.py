from django.db import models

# Create your models here.
class Location(models.Model):
    place = models.CharField(max_length=30)


class Category(models.Model):
    cat = models.CharField(max_length=30)


class Image(models.Model):
    image = models.ImageField(upload_to="gallery/")
    image_name = models.CharField(max_length=10)
    image_description = models.CharField(max_length=30)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    category = models.ManyToManyField(Category)
