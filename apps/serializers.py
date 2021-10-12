# -*- coding: utf-8 -*-
from rest_framework import serializers


class EditorBaseSerializer(serializers.ModelSerializer):
    createTime = serializers.DateTimeField(source="created_at", read_only=True)
    updateTime = serializers.DateTimeField(source="updated_at", read_only=True)
    creator = serializers.StringRelatedField(read_only=True)
    updater = serializers.StringRelatedField(read_only=True)