# Generated by Django 2.2.4 on 2019-08-27 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_auto_20190825_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]