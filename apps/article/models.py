from django.db import models
from ..tag.models import Tag
from ..user.models import EditorBaseModel
from google.cloud import exceptions, storage
from django.dispatch import receiver
from django.conf import settings


class News(EditorBaseModel):
    title = models.CharField(max_length=200, default="", blank=True)
    description = models.TextField(null=True, default="", blank=True)
    detail = models.TextField(null=True, default="", blank=True)
    is_active = models.BooleanField(default=True)
    is_hot = models.BooleanField(default=False)
    hot_at = models.DateTimeField(null=True)
    tags = models.ManyToManyField(Tag)

    objects = models.Manager()


class Image(EditorBaseModel):
    file = models.ImageField(upload_to='articles', null=True)
    size = models.IntegerField(null=True)

    objects = models.Manager()


@receiver(models.signals.post_delete, sender=Image)
def auto_delete_file(sender, instance, **kargs):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(settings.GS_BUCKET_NAME)
    blob = bucket.blob(instance.file.name)
    try:
        blob.delete()
    except Exception as e:
        print(e)