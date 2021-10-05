from django.db import models
from ..user.models import User
from ..tag.models import Tag, Category
from ..user.models import EditorBaseModel


class News(EditorBaseModel):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    detail = models.TextField(null=True)

    tags = models.ManyToManyField(Tag)

    objects = models.Manager()
