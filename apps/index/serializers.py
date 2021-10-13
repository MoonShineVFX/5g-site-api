# -*- coding: utf-8 -*-
import datetime
from rest_framework import serializers
from .models import Setting, About, Banner, Partner
from ..serializers import EditorBaseSerializer


class AboutSerializer(EditorBaseSerializer):
    class Meta:
        model = About
        fields = ('id', 'detail', 'createTime', 'updateTime', 'creator', 'updater')


class BannerListSerializer(EditorBaseSerializer):
    imgUrl = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ('id', 'title', 'imgUrl', 'link', 'priority', 'createTime', 'updateTime', 'creator', 'updater')

    def get_imgUrl(self, instance):
        return "https://storage.googleapis.com/backend-django/{}".format(instance.image) if instance.image else None


class BannerLengthSerializer(serializers.ModelSerializer):
    length = serializers.IntegerField(source='banner_length')

    class Meta:
        model = Setting
        fields = ('length',)

    def validate(self, data):
        length = data['banner_length']
        if length < 5 or length > 10:
            raise serializers.ValidationError("length must between 5 and 10")
        return data


class BannerCreateUpdateSerializer(EditorBaseSerializer):
    file = serializers.ImageField(write_only=True, required=False)
    imgUrl = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ('id', 'title', 'imgUrl', 'file', 'link', 'priority', 'createTime', 'updateTime', 'creator', 'updater')
        read_only = ('id', 'imgUrl', 'createTime', 'updateTime', 'creator', 'updater')

    def create(self, validated_data):
        upload_file = validated_data.get('file', None)
        if upload_file:
            validated_data['size'] = upload_file.size
            validated_data['image'] = validated_data.pop('file')
        resource = self.Meta.model.objects.create(**validated_data)
        return resource

    def update(self, instance, validated_data):
        upload_file = validated_data.get('file', None)
        if upload_file:
            validated_data['size'] = upload_file.size
            validated_data['image'] = validated_data.pop('file')
        return super().update(instance, validated_data)

    def get_imgUrl(self, instance):
        return "https://storage.googleapis.com/backend-django/{}".format(instance.image) if instance.image else None


class PartnerSerializer(EditorBaseSerializer):
    imgUrl = serializers.SerializerMethodField()
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Partner
        fields = ('id',  'imgUrl', 'link', 'name', 'phone', 'email', 'description', 'tags',
                  'createTime', 'updateTime', 'creator', 'updater')
        read_only = ('id', 'imgUrl',)

    def get_imgUrl(self, instance):
        return "https://storage.googleapis.com/backend-django/{}".format(instance.image) if instance.image else None


class PartnerCreateUpdateSerializer(EditorBaseSerializer):
    file = serializers.ImageField(write_only=True, required=False)
    imgUrl = serializers.SerializerMethodField()

    class Meta:
        model = Partner
        fields = ('id', 'imgUrl', 'file', 'link', 'name', 'phone', 'email', 'description', 'tags',
                  'createTime', 'updateTime', 'creator', 'updater')
        read_only = ('id', 'imgUrl',)

    def create(self, validated_data):
        upload_file = validated_data.get('file', None)
        if upload_file:
            validated_data['size'] = upload_file.size
            validated_data['image'] = validated_data.pop('file')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        upload_file = validated_data.get('file', None)
        if upload_file:
            validated_data['size'] = upload_file.size
            validated_data['image'] = validated_data.pop('file')
        return super().update(instance, validated_data)

    def get_imgUrl(self, instance):
        return "https://storage.googleapis.com/backend-django/{}".format(instance.image) if instance.image else None