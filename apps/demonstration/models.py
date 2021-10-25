from django.db import models
from ..user.models import EditorBaseModel


class Demonstration(EditorBaseModel):
    title = models.CharField(max_length=200, default="", blank=True)
    location_url = models.URLField(null=True)
    address = models.CharField(max_length=200, default="", blank=True)
    video_iframe = models.TextField(null=True, default="", blank=True)
    description = models.CharField(max_length=200, default="", blank=True)
    type = models.CharField(max_length=10, default="5g")
    preview = models.ImageField(upload_to='demonstrations/images', null=True)

    contact = models.ForeignKey('Contact', on_delete=models.CASCADE)


class Contact(EditorBaseModel):
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    fax = models.CharField(max_length=50)
    email = models.EmailField()


class Link(EditorBaseModel):
    name = models.CharField(max_length=200)
    url = models.URLField()

    demonstration = models.ForeignKey(Demonstration, related_name="links", on_delete=models.CASCADE)


class Image(EditorBaseModel):
    file = models.ImageField(upload_to='demonstrations/images', null=True)
    size = models.IntegerField(null=True)

    demonstration = models.ForeignKey(Demonstration, related_name="images", on_delete=models.CASCADE)


class File(EditorBaseModel):
    file = models.ImageField(upload_to='demonstrations/files', null=True)
    size = models.IntegerField(null=True)
    type = models.CharField(max_length=50)

    demonstration = models.ForeignKey(Demonstration, related_name="files", on_delete=models.CASCADE)