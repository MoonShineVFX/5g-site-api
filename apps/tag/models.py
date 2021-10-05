from django.db import models
from ..user.models import EditorBaseModel


class Category(models.Model):
    key = models.CharField(max_length=100)
    name = models.CharField(max_length=100)


class Tag(EditorBaseModel):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, models.CASCADE)

