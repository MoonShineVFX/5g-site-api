from django.db import models


class Category(models.Model):
    key = models.CharField(max_length=100)
    name = models.CharField(max_length=100)


class Tag(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, models.CASCADE)

