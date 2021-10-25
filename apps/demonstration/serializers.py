# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Demonstration, Contact, Link, Image, File


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('unit', 'name', 'phone', 'fax', 'email')


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
    imgUrl = serializers.SerializerMethodField()

    class Meta:
        model = Demonstration
        fields = ('id', 'title', 'imgUrl')

    def get_imgUrl(self, instance):
        return "https://storage.googleapis.com/backend-django/{}".format(instance.preview) if instance.preview else None


class WebDemonstrationDetailSerializer(serializers.ModelSerializer):
    locationUrl = serializers.CharField(source="location_url")
    videoIframe = serializers.CharField(source="video_iframe")

    contact = ContactSerializer()
    images = ImageSerializer(many=True, read_only=True)
    links = LinkSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Demonstration
        fields = ('id', 'title', 'locationUrl', 'address', 'description', 'type', 'videoIframe',
                  'contact', 'images', 'links', 'files')