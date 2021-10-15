# -*- coding: utf-8 -*-
from django.utils import timezone
from rest_framework import serializers
from .models import News, Image
from ..serializers import EditorBaseSerializer


class NewsSerializer(EditorBaseSerializer):
    isHot = serializers.BooleanField(source="is_hot")

    class Meta:
        model = News
        fields = ('id', 'title', 'description', "detail", 'tags', "isHot",
                  'createTime', 'updateTime', 'creator', 'updater')

    def is_hot_updater(self, validated_data):
        is_hot = validated_data.get('is_hot', None)
        if is_hot is not None:
            if is_hot:
                validated_data['hot_at'] = timezone.now()
            else:
                validated_data['hot_at'] = None
        return validated_data

    def create(self, validated_data):
        validated_data = self.is_hot_updater(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data = self.is_hot_updater(validated_data)
        return super().update(instance, validated_data)


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
    isHot = serializers.BooleanField(source="is_hot")

    class Meta:
        model = News
        fields = ('id', 'title', 'description', 'categoryId', 'categoryKey', 'categoryName', 'tags', "isHot",
                  'createTime', 'updateTime', 'creator', 'updater')

    def get_categoryId(self, instance):
        return instance.tags.all()[0].category_id if instance.tags else None

    def get_categoryKey(self, instance):
        return instance.tags.all()[0].category.key if instance.tags else None

    def get_categoryName(self, instance):
        return instance.tags.all()[0].category.name if instance.tags else None


class NewsDetailSerializer(EditorBaseSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    isHot = serializers.BooleanField(source="is_hot")

    class Meta:
        model = News
        fields = ('id', 'title', 'description', 'detail', 'tags', "isHot",
                  'createTime', 'updateTime', 'creator', 'updater')

