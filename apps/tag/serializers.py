# -*- coding: utf-8 -*-
import datetime
from rest_framework import serializers
from .models import Tag, Category


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagWithCategorySerializer(serializers.ModelSerializer):
    categoryId = serializers.IntegerField(source="category_id")
    categoryKey = serializers.SerializerMethodField()
    categoryName = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'categoryId', 'categoryKey', 'categoryName')

    def get_categoryKey(self, instance):
        return instance.category.key if instance.category else None

    def get_categoryName(self, instance):
        return instance.category.name if instance.category else None


class TagNameCategorySerializer(serializers.Serializer):
    name = serializers.CharField()
    categoryId = serializers.IntegerField()


class TagListCreateSerializer(serializers.Serializer):
    tag = serializers.ListSerializer(child=TagNameCategorySerializer())

    def create(self, validated_data):
        tags = [Tag(name=tag['name'], category_id=tag['categoryId']) for tag in validated_data['tag']]
        created_tags = Tag.objects.bulk_create(tags)
        return created_tags[0]


class TagUpdateSerializer(serializers.ModelSerializer):
    categoryId = serializers.IntegerField(source="category_id")
    categoryKey = serializers.SerializerMethodField()
    categoryName = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'categoryId', 'categoryKey', 'categoryName', )

    def get_categoryKey(self, instance):
        return instance.category.key if instance.category else None

    def get_categoryName(self, instance):
        return instance.category.name if instance.category else None