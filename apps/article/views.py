from django.utils import timezone
from .models import News
from . import serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..shortcuts import WebCreateView, WebUpdateView


class NewsList(ListAPIView):
    serializer_class = serializers.NewsListSerializer
    queryset = News.objects.prefetch_related('tags', 'tags__category').all()

    def post(self, request, *args, **kwargs):
        return self.get(self, request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"list": serializer.data})


class NewsDetail(RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = serializers.NewsDetailSerializer


class NewsCreate(WebCreateView):
    serializer_class = serializers.NewsSerializer
    queryset = News.objects.all()


class NewsUpdate(WebUpdateView):
    serializer_class = serializers.NewsSerializer
    queryset = News.objects.all()

    def get_object(self):
        return get_object_or_404(News, id=self.request.data.get('id', None))