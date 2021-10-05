# -*- coding: utf-8 -*-
import datetime
from rest_framework import serializers
from .models import News, Image


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'description', "detail", 'tags')


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


class NewsListSerializer(serializers.ModelSerializer):
    categoryId = serializers.SerializerMethodField()
    categoryKey = serializers.SerializerMethodField()
    categoryName = serializers.SerializerMethodField()
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    createTime = serializers.DateTimeField(source='created_at')
    updateTime = serializers.DateTimeField(source='updated_at')

    class Meta:
        model = News
        fields = ('id', 'title', 'description', 'categoryId', 'categoryKey', 'categoryName', 'tags',
                  'createTime', 'updateTime')

    def get_categoryId(self, instance):
        return instance.tags.all()[0].category_id if instance.tags else None

    def get_categoryKey(self, instance):
        return instance.tags.all()[0].category.key if instance.tags else None

    def get_categoryName(self, instance):
        return instance.tags.all()[0].category.name if instance.tags else None


class NewsDetailSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = News
        fields = ('id', 'title', 'description', 'detail', 'tags',)

