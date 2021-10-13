from django.db import models
from ..tag.models import Tag
from ..user.models import EditorBaseModel


class News(EditorBaseModel):
    title = models.CharField(max_length=200, default="", blank=True)
    description = models.CharField(max_length=200, default="", blank=True)
    detail = models.TextField(null=True, default="", blank=True)

    tags = models.ManyToManyField(Tag)

    objects = models.Manager()


class Image(EditorBaseModel):
    file = models.ImageField(upload_to='articles', null=True)
    size = models.IntegerField(null=True)

    objects = models.Manager()