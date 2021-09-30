# -*- coding: utf-8 -*-
import datetime
from rest_framework import serializers
from .models import Banner, Partner, Setting


class BannerListSerializer(serializers.ModelSerializer):
    imgUrl = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ('id', 'title', 'imgUrl', 'link', 'priority')

    def get_imgUrl(self, instance):
        return "https://storage.googleapis.com/backend-django/{}".format(instance.image) if instance.image else None


class BannerLengthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ('length',)

    def validate(self, data):
        length = data['length']
        if length < 5 or length > 10:
            raise serializers.ValidationError("length must between 5 and 10")
        return data


class BannerCreateUpdateSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(write_only=True)
    imgUrl = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ('id', 'title', 'imgUrl', 'file', 'link', 'priority')
        read_only = ('id', 'token', 'imgUrl',)

    def create(self, validated_data):
        upload_file = validated_data['file']
        validated_data['size'] = upload_file.size
        validated_data['image'] = validated_data.pop('file')
        resource = self.Meta.model.objects.create(**validated_data)
        return resource

    def update(self, instance, validated_data):
        upload_file = validated_data['file']
        if upload_file:
            validated_data['size'] = upload_file.size
            validated_data['image'] = validated_data.pop('file')
        return super().update(instance, validated_data)

    def get_imgUrl(self, instance):
        return "https://storage.googleapis.com/backend-django/{}".format(instance.image) if instance.image else None


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'