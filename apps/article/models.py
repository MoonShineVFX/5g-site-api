from django.db import models
from ..user.models import User
from ..tag.models import Tag, Category


class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    detail = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    objects = models.Manager()
