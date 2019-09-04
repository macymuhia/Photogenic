from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import urllib, os
from urllib.parse import urlparse
from fontawesome.fields import IconField

# Create your models here.
class UserProfileManager(models.Manager):
    pass


# class UserProfile(models.Model):
#     # user = models.OneToOneField(User)
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     description = models.CharField(max_length=100, default="")
#     city = models.CharField(max_length=100, default="")
#     website = models.URLField(default="")
#     phoneNumber = models.IntegerField(default=0)
#     image = models.ImageField(upload_to="profile_image", blank=True)

#     def __str__(self):
#         return self.user.username


# def createProfile(sender, **kwargs):
#     if kwargs["created"]:
#         user_profile = UserProfile.objects.created(user=kwargs["instance"])

#         post_save.connect(createProfile, sender=User)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="gallery/")
    email_confirmed = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


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
