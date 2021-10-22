# -*- coding: utf-8 -*-
import datetime
from rest_framework import serializers
from .models import Tag, Category
from ..serializers import EditorBaseSerializer


class CategoryMixin(serializers.Serializer):
    categoryId = serializers.SerializerMethodField()
    categoryKey = serializers.SerializerMethodField()
    categoryName = serializers.SerializerMethodField()

    def get_categoryId(self, instance):
        return instance.tags.all()[0].category_id if instance.tags.all() else None

    def get_categoryKey(self, instance):
        return instance.tags.all()[0].category.key if instance.tags.all() else None

    def get_categoryName(self, instance):
        return instance.tags.all()[0].category.name if instance.tags.all() else None


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TagNameOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagWithCategorySerializer(EditorBaseSerializer):
    categoryId = serializers.IntegerField(source="category_id")
    categoryKey = serializers.SerializerMethodField()
    categoryName = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'categoryId', 'categoryKey', 'categoryName',
                  'createTime', 'updateTime', 'creator', 'updater')

    def get_categoryKey(self, instance):
        return instance.category.key if instance.category else None

    def get_categoryName(self, instance):
        return instance.category.name if instance.category else None


class TagNameCategorySerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=True)
    categoryId = serializers.IntegerField(required=False, allow_null=True)


class TagListCreateSerializer(serializers.Serializer):
    tags = serializers.ListSerializer(child=TagNameCategorySerializer())

    def create(self, validated_data):
        print(validated_data["creator_id"])
        tags = [
            Tag(name=tag['name'], category_id=tag['categoryId'], creator_id=validated_data["creator_id"])
            for tag in validated_data['tags']]
        created_tags = Tag.objects.bulk_create(tags)
        return created_tags[0]


class TagUpdateSerializer(EditorBaseSerializer):
    categoryId = serializers.IntegerField(source="category_id")
    categoryKey = serializers.SerializerMethodField()
    categoryName = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'categoryId', 'categoryKey', 'categoryName',
                  'createTime', 'updateTime', 'creator', 'updater')

    def get_categoryKey(self, instance):
        return instance.category.key if instance.category else None

    def get_categoryName(self, instance):
        return instance.category.name if instance.category else None