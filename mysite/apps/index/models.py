import os
from django.db import models
from ..tag.models import Tag
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


class Setting(models.Model):
    length = models.IntegerField(default=5)

    objects = models.Manager()


class Banner(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField()
    image = models.ImageField(upload_to='banners', null=True)
    priority = models.IntegerField(default=1)
    size = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    objects = models.Manager()


class Partner(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    description = models.CharField(max_length=80)
    link = models.URLField()
    image = models.ImageField(upload_to='partners', null=True)
    size = models.IntegerField(null=True)
    tag = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()


@receiver(models.signals.pre_save, sender=Banner)
@receiver(models.signals.pre_save, sender=Partner)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `File` object is updated
    with new file.
    """
    if not instance.id:
        return False

    old_file = None
    new_file = None
    try:
        Model = type(instance)
        old_file = Model.objects.get(id=instance.id).image
        new_file = instance.image
    except ObjectDoesNotExist:
        return False

    if not old_file:
        return False

    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)