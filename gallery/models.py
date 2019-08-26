from django.db import models

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
    image_description = models.CharField(max_length=30)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    category = models.ManyToManyField(Category)
    created_on = models.DateTimeField(auto_now_add=True)

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
        return cls.objects.filter(title__icontains=search_term)

    def __str__(self):
        return self.image_name
