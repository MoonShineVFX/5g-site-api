# -*- coding: utf-8 -*-
from django.utils import timezone
from rest_framework import serializers
from .models import Policy
from ..serializers import EditorBaseSerializer, EditTimeBaseSerializer
from ..tag.serializers import TagNameOnlySerializer, CategoryMixin
from ..demonstration.serializers import ContactSerializer


class WebPolicyListSerializer(serializers.ModelSerializer):
    titleSecondary = serializers.CharField(source="title_secondary")
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Policy
        fields = ('id', 'title', 'titleSecondary', 'description', 'tags')


class WebPolicyDetailSerializer(EditTimeBaseSerializer, CategoryMixin):
    applicationWay = serializers.CharField(source="application_way")
    applicationObject = serializers.CharField(source="application_object")
    amountQuota = serializers.CharField(source="amount_quota")

    tags = TagNameOnlySerializer(many=True, read_only=True)
    contact = ContactSerializer()

    class Meta:
        model = Policy
        fields = ('id', 'title', 'description', 'tags', 'contact',
                  'categoryKey', 'categoryName', 'createTime', 'updateTime',
                  'applicationWay', 'applicationObject', 'amountQuota', 'link',)


class PolicyListSerializer(EditorBaseSerializer, CategoryMixin):
    titleSecondary = serializers.CharField(source="title_secondary")
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    contact = ContactSerializer()

    class Meta:
        model = Policy
        fields = ('id', 'title', 'titleSecondary', 'description', 'categoryKey', 'tags', 'contact', 'link',
                  'createTime', 'updateTime', 'creator', 'updater')


class PolicyDetailSerializer(EditorBaseSerializer, CategoryMixin):
    applicationWay = serializers.CharField(source="application_way")
    applicationObject = serializers.CharField(source="application_object")
    amountQuota = serializers.CharField(source="amount_quota")

    tags = TagNameOnlySerializer(many=True, read_only=True)
    contact = ContactSerializer()

    class Meta:
        model = Policy
        fields = ('id', 'title', 'description', 'tags', 'contact',
                  'categoryKey', 'categoryName',
                  'applicationWay', 'applicationObject', 'amountQuota', 'link',
                  'createTime', 'updateTime', 'creator', 'updater')


class PolicyCreateUpdateSerializer(EditorBaseSerializer):
    titleSecondary = serializers.CharField(source="title_secondary")

    contactUnit = serializers.CharField(source="contact_name", write_only=True)
    contactName = serializers.CharField(source="contact_unit", write_only=True)
    contactPhone = serializers.CharField(source="contact_phone", write_only=True)
    contactFax = serializers.CharField(source="contact_fax", write_only=True)
    contactEmail = serializers.CharField(source="contact_email", write_only=True)

    applicationWay = serializers.CharField(source="application_way", required=False, allow_null=True, allow_blank=True)
    applicationObject = serializers.CharField(source="application_object", required=False, allow_null=True, allow_blank=True)
    amountQuota = serializers.CharField(source="amount_quota", required=False, allow_null=True, allow_blank=True)

    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Policy
        fields = ('id', 'title', 'titleSecondary', 'description', 'tags', 'link',
                  'contactUnit', 'contactName', 'contactPhone', 'contactFax', 'contactEmail',
                  'applicationWay', 'applicationObject', 'amountQuota',
                  'contact',
                  'createTime', 'updateTime', 'creator', 'updater')