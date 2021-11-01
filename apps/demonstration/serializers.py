# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Demonstration, Image, File
from ..serializers import EditorBaseSerializer


class ContactSerializer(serializers.Serializer):
    unit = serializers.CharField(source="contact_name")
    name = serializers.CharField(source="contact_unit")
    phone = serializers.CharField(source="contact_phone")
    fax = serializers.CharField(source="contact_fax")
    email = serializers.CharField(source="contact_email")


class ImageSerializer(serializers.ModelSerializer):
    imgUrl = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('id', 'imgUrl', )

    def get_imgUrl(self, instance):
        return "https://storage.googleapis.com/backend-django/{}".format(instance.file) if instance.file else None


class FileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ('id', 'name', 'size', 'type', 'url')

    def get_name(self, instance):
        return instance.file.__str__().rsplit('/', 1)[1] if instance.file else None

    def get_url(self, instance):
        return "https://storage.googleapis.com/backend-django/{}".format(instance.file) if instance.file else None


class ImageUploadSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(write_only=True)
    imgUrl = serializers.SerializerMethodField()
    demoPlaceId = serializers.IntegerField(source="demonstration_id")

    class Meta:
        model = Image
        fields = ('id', 'file', 'imgUrl', 'demoPlaceId')

    def create(self, validated_data):
        upload_file = validated_data['file']
        validated_data['size'] = upload_file.size
        return super().create(validated_data)

    def get_imgUrl(self, instance):
        return "https://storage.googleapis.com/backend-django/{}".format(instance.file) if instance.file else None


class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)
    name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    demoPlaceId = serializers.IntegerField(source="demonstration_id")

    def create(self, validated_data):
        upload_file = validated_data['file']
        validated_data['size'] = upload_file.size
        validated_data['type'] = upload_file.content_type
        return super().create(validated_data)

    class Meta:
        model = File
        fields = ('id', 'name', 'file', 'url', 'demoPlaceId')

    def get_name(self, instance):
        return instance.file.__str__().rsplit('/', 1)[1] if instance.file else None

    def get_url(self, instance):
        return "https://storage.googleapis.com/backend-django/{}".format(instance.file) if instance.file else None


class WebDemonstrationListSerializer(serializers.ModelSerializer):
    imgUrl = serializers.SerializerMethodField()

    class Meta:
        model = Demonstration
        fields = ('id', 'title', 'imgUrl')

    def get_imgUrl(self, instance):
        return "https://storage.googleapis.com/backend-django/{}".format(instance.thumb) if instance.thumb else None


class WebDemonstrationDetailSerializer(serializers.ModelSerializer):
    locationUrl = serializers.CharField(source="location_url")
    videoIframe = serializers.CharField(source="video_iframe")
    websiteName = serializers.CharField(source="website_name")
    websiteUrl = serializers.URLField(source="website_url")
    byMRT = serializers.CharField(source="by_mrt")
    byDrive = serializers.CharField(source="by_drive")

    contact = ContactSerializer()
    images = ImageSerializer(many=True)

    files = FileSerializer(many=True)

    class Meta:
        model = Demonstration
        fields = ('id', 'title', 'locationUrl', 'address', 'description', 'type', 'videoIframe',
                  'websiteName', 'websiteUrl', 'byMRT', 'byDrive', 'contact', 'images', 'files')


class DemonstrationListSerializer(EditorBaseSerializer):
    imgUrl = serializers.SerializerMethodField()
    contact = ContactSerializer()

    class Meta:
        model = Demonstration
        fields = ('id', 'title', 'imgUrl', 'address', 'type', 'contact',
                  'createTime', 'updateTime', 'creator', 'updater')

    def get_imgUrl(self, instance):
        return "https://storage.googleapis.com/backend-django/{}".format(instance.thumb) if instance.thumb else None


class DemonstrationDetailSerializer(WebDemonstrationDetailSerializer, EditorBaseSerializer):
    imgUrl = serializers.SerializerMethodField()

    class Meta:
        model = Demonstration
        fields = ('id', 'title', 'locationUrl', 'address', 'description', 'type', 'videoIframe', 'imgUrl',
                  'websiteName', 'websiteUrl', 'byMRT', 'byDrive', 'contact', 'images', 'files',
                  'createTime', 'updateTime', 'creator', 'updater')

    def get_imgUrl(self, instance):
        return "https://storage.googleapis.com/backend-django/{}".format(instance.thumb) if instance.thumb else None


class DemonstrationCreateUpdateSerializer(EditorBaseSerializer):
    locationUrl = serializers.CharField(source="location_url", required=False)
    videoIframe = serializers.CharField(source="video_iframe", required=False)

    websiteName = serializers.CharField(source="website_name")
    websiteUrl = serializers.URLField(source="website_url", allow_null=True, allow_blank=True)

    contactUnit = serializers.CharField(source="contact_name")
    contactName = serializers.CharField(source="contact_unit")
    contactPhone = serializers.CharField(source="contact_phone")
    contactFax = serializers.CharField(source="contact_fax")
    contactEmail = serializers.CharField(source="contact_email")
    byMRT = serializers.CharField(source="by_mrt", allow_null=True)
    byDrive = serializers.CharField(source="by_drive", allow_null=True)

    class Meta:
        model = Demonstration
        fields = ('id', 'title', 'locationUrl', 'address', 'description', 'type', 'videoIframe',
                  'websiteName', 'websiteUrl', 'thumb',
                  'contactUnit', 'contactName', 'contactPhone', 'contactFax', 'contactEmail', 'byMRT', 'byDrive',
                  'createTime', 'updateTime', 'creator', 'updater')