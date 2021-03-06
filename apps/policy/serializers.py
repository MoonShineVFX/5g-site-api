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
    websiteName = serializers.CharField(source="website_name")

    tags = TagNameOnlySerializer(many=True, read_only=True)
    contact = ContactSerializer()

    class Meta:
        model = Policy
        fields = ('id', 'title', 'description', 'tags', 'contact',
                  'categoryKey', 'categoryName', 'createTime', 'updateTime',
                  'applicationWay', 'applicationObject', 'amountQuota', 'websiteName', 'link',)


class PolicyListSerializer(EditorBaseSerializer, CategoryMixin):
    titleSecondary = serializers.CharField(source="title_secondary")
    applicationWay = serializers.CharField(source="application_way")
    applicationObject = serializers.CharField(source="application_object")
    amountQuota = serializers.CharField(source="amount_quota")
    websiteName = serializers.CharField(source="website_name")

    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    contact = ContactSerializer()

    class Meta:
        model = Policy
        fields = ('id', 'title', 'titleSecondary', 'applicationWay', 'applicationObject', 'amountQuota',
                  'description', 'categoryKey', 'tags', 'contact', 'websiteName', 'link',
                  'createTime', 'updateTime', 'creator', 'updater')


class PolicyDetailSerializer(EditorBaseSerializer, CategoryMixin):
    applicationWay = serializers.CharField(source="application_way")
    applicationObject = serializers.CharField(source="application_object")
    amountQuota = serializers.CharField(source="amount_quota")
    websiteName = serializers.CharField(source="website_name")

    tags = TagNameOnlySerializer(many=True, read_only=True)
    contact = ContactSerializer()

    class Meta:
        model = Policy
        fields = ('id', 'title', 'description', 'tags', 'contact',
                  'categoryKey', 'categoryName',
                  'applicationWay', 'applicationObject', 'amountQuota', 'websiteName', 'link',
                  'createTime', 'updateTime', 'creator', 'updater')


class PolicyCreateUpdateSerializer(EditorBaseSerializer):
    titleSecondary = serializers.CharField(source="title_secondary")
    websiteName = serializers.CharField(source="website_name", required=False, allow_null=True, allow_blank=True)

    contactUnit = serializers.CharField(source="contact_name", write_only=True, required=False, allow_null=True, allow_blank=True)
    contactName = serializers.CharField(source="contact_unit", write_only=True, required=False, allow_null=True, allow_blank=True)
    contactPhone = serializers.CharField(source="contact_phone", write_only=True, required=False, allow_null=True, allow_blank=True)
    contactFax = serializers.CharField(source="contact_fax", write_only=True, required=False, allow_null=True, allow_blank=True)
    contactEmail = serializers.CharField(source="contact_email", write_only=True, required=False, allow_null=True, allow_blank=True)

    applicationWay = serializers.CharField(source="application_way", required=False, allow_null=True, allow_blank=True)
    applicationObject = serializers.CharField(source="application_object", required=False, allow_null=True, allow_blank=True)
    amountQuota = serializers.CharField(source="amount_quota", required=False, allow_null=True, allow_blank=True)

    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Policy
        fields = ('id', 'title', 'titleSecondary', 'description', 'tags', 'websiteName', 'link',
                  'contactUnit', 'contactName', 'contactPhone', 'contactFax', 'contactEmail',
                  'applicationWay', 'applicationObject', 'amountQuota',
                  'contact',
                  'createTime', 'updateTime', 'creator', 'updater')