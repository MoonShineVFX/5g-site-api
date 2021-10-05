# -*- coding: utf-8 -*-
import datetime
from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'description', "detail", 'tags')


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

