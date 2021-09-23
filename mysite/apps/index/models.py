from django.db import models
from ..tag.models import Tag


class Banner(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField()
    image = models.ImageField(upload_to='banners', null=True)
    priority = models.ImageField(default=1)


class Partner(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    description = models.CharField(max_length=80)
    link = models.URLField()
    image = models.ImageField(upload_to='partners', null=True)
    tag = models.ManyToManyField(Tag)
