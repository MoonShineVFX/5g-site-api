import os
from django.db import models
from ..tag.models import Tag
from ..user.models import EditorBaseModel
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage


class Setting(EditorBaseModel):
    banner_length = models.IntegerField(default=5)

    objects = models.Manager()


class About(EditorBaseModel):
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
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    description = models.CharField(max_length=80)
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
        if default_storage.exists(old_file.path):
            default_storage.delete(old_file.path)