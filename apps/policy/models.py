from django.db import models
from ..user.models import EditorBaseModel
from ..tag.models import Tag


class Policy(EditorBaseModel):
    title = models.CharField(max_length=200, default="", blank=True)
    title_secondary = models.CharField(max_length=200, default="", blank=True)
    description = models.CharField(max_length=200, default="", blank=True)
    application_way = models.TextField(null=True, default="", blank=True)
    application_object = models.TextField(null=True, default="", blank=True)
    amount_quota = models.CharField(max_length=50, default="", blank=True)
    link = models.URLField(null=True)

    contact = models.ForeignKey('Contact', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)


class Contact(EditorBaseModel):
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    fax = models.CharField(max_length=50)
    email = models.EmailField()
