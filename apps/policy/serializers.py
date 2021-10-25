# -*- coding: utf-8 -*-
from django.utils import timezone
from rest_framework import serializers
from .models import Policy, Contact
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
