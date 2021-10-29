from django.db import models
from ..user.models import EditorBaseModel
from ..tag.models import Tag


class Policy(EditorBaseModel):
    title = models.CharField(max_length=200, default="", blank=True)
    title_secondary = models.CharField(max_length=200, default="", blank=True)
    description = models.CharField(max_length=200, default="", blank=True)
    application_way = models.TextField(null=True, default="", blank=True)
    application_object = models.TextField(null=True, default="", blank=True)
    amount_quota = models.CharField(max_length=50, default="", blank=True)
    link = models.URLField(null=True)

    contact_name = models.CharField(max_length=200, null=True)
    contact_unit = models.CharField(max_length=200, null=True)
    contact_phone = models.CharField(max_length=50, null=True)
    contact_fax = models.CharField(max_length=50, null=True)
    contact_email = models.EmailField(null=True)

    tags = models.ManyToManyField(Tag)

    @property
    def contact(self):
        return {
            "contact_name": self.contact_name,
            "contact_unit": self.contact_unit,
            "contact_phone": self.contact_phone,
            "contact_fax": self.contact_fax,
            "contact_email": self.contact_email
        }