# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Demonstration, Link, Image, File
from ..serializers import EditorBaseSerializer


class ContactSerializer(serializers.Serializer):
    unit = serializers.CharField(source="contact_name")
    name = serializers.CharField(source="contact_unit")
    phone = serializers.CharField(source="contact_phone")
    fax = serializers.CharField(source="contact_fax")
    email = serializers.CharField(source="contact_email")


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('name', 'url')


class ImageSerializer(serializers.ModelSerializer):
    imgUrl = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('id', 'imgUrl')

    def get_imgUrl(self, instance):
        return "https://storage.googleapis.com/backend-django/{}".format(instance.file) if instance.file else None


class FileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ('name', 'size', 'type', 'url')

    def get_name(self, instance):
        return instance.file.__str__().rsplit('/', 1)[1] if instance.file else None

    def get_url(self, instance):
        return "https://storage.googleapis.com/backend-django/{}".format(instance.file) if instance.file else None


class WebDemonstrationListSerializer(serializers.ModelSerializer):
    imgUrl = serializers.CharField(source="thumb")

    class Meta:
        model = Demonstration
        fields = ('id', 'title', 'imgUrl')


class WebDemonstrationDetailSerializer(serializers.ModelSerializer):
    locationUrl = serializers.CharField(source="location_url")
    videoIframe = serializers.CharField(source="video_iframe")

    contact = ContactSerializer()
    images = ImageSerializer(many=True)
    links = LinkSerializer(many=True)
    files = FileSerializer(many=True)

    class Meta:
        model = Demonstration
        fields = ('id', 'title', 'locationUrl', 'address', 'description', 'type', 'videoIframe',
                  'contact', 'images', 'links', 'files')


class DemonstrationListSerializer(EditorBaseSerializer):
    imgUrl = serializers.CharField(source="thumb")
    contact = ContactSerializer()

    class Meta:
        model = Demonstration
        fields = ('id', 'title', 'imgUrl', 'address', 'type', 'contact',
                  'createTime', 'updateTime', 'creator', 'updater')


class DemonstrationDetailSerializer(WebDemonstrationDetailSerializer, EditorBaseSerializer):
    imgUrl = serializers.CharField(source="thumb")

    class Meta:
        model = Demonstration
        fields = ('id', 'title', 'locationUrl', 'address', 'description', 'type', 'videoIframe', 'imgUrl',
                  'contact', 'images', 'links', 'files',
                  'createTime', 'updateTime', 'creator', 'updater')


class DemonstrationCreateUpdateSerializer(EditorBaseSerializer):
    locationUrl = serializers.CharField(source="location_url")
    videoIframe = serializers.CharField(source="video_iframe")
    contactUnit = serializers.CharField(source="contact_name")
    contactName = serializers.CharField(source="contact_unit")
    contactPhone = serializers.CharField(source="contact_phone")
    contactFax = serializers.CharField(source="contact_fax")
    contactEmail = serializers.CharField(source="contact_email")

    class Meta:
        model = Demonstration
        fields = ('id', 'title', 'locationUrl', 'address', 'description', 'type', 'videoIframe', 'thumb',
                  'contactUnit', 'contactName', 'contactPhone', 'contactFax', 'contactEmail',
                  'createTime', 'updateTime', 'creator', 'updater')