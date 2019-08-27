from django.test import TestCase
from gallery.models import Image


class ImageTest(TestCase):
    def test_save_image(self):
        im = Image()
        im.image_name = "home"
        im.image_url = File(open("/tmp/uplods/home.jpg"))
        im.save()

        h_image = im.objects.get(id=1).image_url.path
        self.failUnless(open(h_image), "file not found")

