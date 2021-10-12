# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import News, Image
from ..serializers import EditorBaseSerializer


class NewsSerializer(EditorBaseSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'description', "detail", 'tags', 'createTime', 'updateTime', 'creator', 'updater')


class ImageSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(write_only=True)
    imgUrl = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('file', 'imgUrl')

    def create(self, validated_data):
        upload_file = validated_data['file']
        validated_data['size'] = upload_file.size
        return super().create(validated_data)

    def get_imgUrl(self, instance):
        return "https://storage.googleapis.com/backend-django/{}".format(instance.file) if instance.file else None


class NewsListSerializer(EditorBaseSerializer):
    categoryId = serializers.SerializerMethodField()
    categoryKey = serializers.SerializerMethodField()
    categoryName = serializers.SerializerMethodField()
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = News
        fields = ('id', 'title', 'description', 'categoryId', 'categoryKey', 'categoryName', 'tags',
                  'createTime', 'updateTime', 'creator', 'updater')

    def get_categoryId(self, instance):
        return instance.tags.all()[0].category_id if instance.tags else None

    def get_categoryKey(self, instance):
        return instance.tags.all()[0].category.key if instance.tags else None

    def get_categoryName(self, instance):
        return instance.tags.all()[0].category.name if instance.tags else None


class NewsDetailSerializer(EditorBaseSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = News
        fields = ('id', 'title', 'description', 'detail', 'tags', 'createTime', 'updateTime', 'creator', 'updater')

