# -*- coding: utf-8 -*-
from django.utils import timezone
from rest_framework import serializers
from .models import News, Image
from ..serializers import EditorBaseSerializer, EditTimeBaseSerializer
from ..tag.serializers import TagNameOnlySerializer, CategoryMixin


class NewsSerializer(EditorBaseSerializer):
    isHot = serializers.BooleanField(source="is_hot")
    isActive = serializers.BooleanField(source="is_active", required=False)

    class Meta:
        model = News
        fields = ('id', 'title', 'description', "detail", 'tags', "isHot", "isActive",
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


class NewsListSerializer(EditorBaseSerializer, CategoryMixin):
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    isHot = serializers.BooleanField(source="is_hot")

    class Meta:
        model = News
        fields = ('id', 'title', 'description', 'categoryId', 'categoryKey', 'categoryName', 'tags', "isHot",
                  'createTime', 'updateTime', 'creator', 'updater')


class NewsDetailSerializer(EditorBaseSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    isHot = serializers.BooleanField(source="is_hot")

    class Meta:
        model = News
        fields = ('id', 'title', 'description', 'detail', 'tags', "isHot",
                  'createTime', 'updateTime', 'creator', 'updater')


class WebNewsListSerializer(serializers.ModelSerializer):
    createTime = serializers.SerializerMethodField()
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = News
        fields = ('id', 'title', 'description', 'createTime', 'tags')

    def get_createTime(self, instance):
        return instance.created_at if instance.created_at else ""


class OtherNewsSerializer(serializers.ModelSerializer):
    createTime = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ('id', 'title', 'description', 'createTime')

    def get_createTime(self, instance):
        return instance.created_at if instance.created_at else ""


class WebNewsDetailSerializer(EditTimeBaseSerializer, CategoryMixin):
    tags = TagNameOnlySerializer(many=True, read_only=True)
    otherNews = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ('id', 'title', 'detail', 'tags', 'categoryKey', 'categoryName',
                  'createTime', 'updateTime', 'otherNews',)

    def get_otherNews(self, instance):
        data = []
        prev = None
        next = None

        category_id = instance.tags.all()[0].category_id if instance.tags.all() else None
        if category_id:
            prev = News.objects.filter(id__lt=instance.id, tags__category_id=category_id).order_by('id').last()
            next = News.objects.filter(id__gt=instance.id, tags__category_id=category_id).order_by('id').first()

        if prev:
            data.append(OtherNewsSerializer(prev).data)
        if next:
            data.append(OtherNewsSerializer(next).data)

        return data