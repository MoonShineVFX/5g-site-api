from django.db import models
from ..user.models import EditorBaseModel
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from google.cloud import exceptions, storage
from django.conf import settings


class Demonstration(EditorBaseModel):
    title = models.CharField(max_length=200, default="", blank=True)
    location_url = models.TextField(null=True)
    address = models.CharField(max_length=200, default="", blank=True)
    video_iframe = models.TextField(null=True, default="", blank=True)
    description = models.TextField(null=True, default="", blank=True)
    type = models.CharField(max_length=10, default="5g")
    thumb = models.ImageField(upload_to='demonstrations/images', null=True)
    website_url = models.URLField(null=True)
    website_name = models.CharField(max_length=50, null=True)

    contact_name = models.CharField(max_length=200, null=True)
    contact_unit = models.CharField(max_length=200, null=True)
    contact_phone = models.CharField(max_length=50, null=True)
    contact_fax = models.CharField(max_length=50, null=True)
    contact_email = models.EmailField(null=True)

    by_mrt = models.TextField(null=True, default="", blank=True)
    by_drive = models.TextField(null=True, default="", blank=True)

    @property
    def contact(self):
        return {
            "contact_name": self.contact_name,
            "contact_unit": self.contact_unit,
            "contact_phone": self.contact_phone,
            "contact_fax": self.contact_fax,
            "contact_email": self.contact_email
        }


class Image(EditorBaseModel):
    file = models.ImageField(upload_to='demonstrations/images', null=True)
    size = models.IntegerField(null=True)

    demonstration = models.ForeignKey(Demonstration, related_name="images", on_delete=models.CASCADE)


class File(EditorBaseModel):
    file = models.FileField(upload_to='demonstrations/files', null=True)
    size = models.IntegerField(null=True)
    type = models.CharField(max_length=255)

    demonstration = models.ForeignKey(Demonstration, related_name="files", on_delete=models.CASCADE)


@receiver(models.signals.pre_save, sender=Demonstration)
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
        old_file = Model.objects.get(id=instance.id).thumb
        new_file = instance.thumb
    except ObjectDoesNotExist:
        return False

    if not old_file:
        return False

    if not old_file == new_file:
        try:
            old_file.storage.delete(name=old_file.name)
        except exceptions.NotFound as e:
            print(e)


@receiver(models.signals.post_delete, sender=Image)
@receiver(models.signals.post_delete, sender=File)
def auto_delete_file(sender, instance, **kargs):
    file = instance.file
    if file:
        try:
            file.storage.delete(name=file.name)
        except exceptions.NotFound as e:
            print(e)