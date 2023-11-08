import os
from django.db import models
from ..tag.models import Tag
from ..user.models import EditorBaseModel
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from google.cloud import exceptions


class Setting(EditorBaseModel):
    banner_length = models.IntegerField(default=5)
    loop_time = models.IntegerField(default=6)
    objects = models.Manager()


class About(EditorBaseModel):
    detail = models.TextField(default="")

    objects = models.Manager()


class Privacy(EditorBaseModel):
    title = models.CharField(max_length=100, null=True)
    detail = models.TextField(default="")

    objects = models.Manager()


class Security(EditorBaseModel):
    title = models.CharField(max_length=100, null=True)
    detail = models.TextField(default="")

    objects = models.Manager()


class Banner(EditorBaseModel):
    title = models.CharField(max_length=100, null=True)
    link = models.URLField()
    image = models.ImageField(upload_to='banners', null=True)
    priority = models.IntegerField(default=1)
    size = models.IntegerField(null=True)

    objects = models.Manager()


class Partner(EditorBaseModel):
    name = models.CharField(max_length=100)
    name_english = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    description = models.CharField(max_length=150)
    link = models.URLField()
    image = models.ImageField(upload_to='partners', null=True)
    size = models.IntegerField(null=True)
    tags = models.ManyToManyField(Tag)

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
        try:
            old_file.storage.delete(name=old_file.name)
        except exceptions.NotFound as e:
            print(e)


@receiver(models.signals.pre_delete, sender=Banner)
@receiver(models.signals.pre_delete, sender=Partner)
def auto_delete_file(sender, instance, **kargs):
    file = instance.image
    if file:
        try:
            file.storage.delete(name=file.name)
        except Exception:
            pass