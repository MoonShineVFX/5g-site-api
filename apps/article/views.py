from .models import News, Image
from ..tag.models import Tag
from . import serializers
from ..tag.serializers import TagNameOnlySerializer
from ..pagination import NewsPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from ..shortcuts import WebCreateView, WebUpdateView, PostCreateView


class NewsList(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.NewsListSerializer
    queryset = News.objects.select_related("creator", "updater").prefetch_related('tags', 'tags__category').all()

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
    permission_classes = (IsAuthenticated, )
    queryset = News.objects.select_related("creator", "updater").all()
    serializer_class = serializers.NewsDetailSerializer


class NewsCreate(WebCreateView):
    serializer_class = serializers.NewsSerializer
    queryset = News.objects.select_related("creator", "updater").all()


class NewsUpdate(WebUpdateView):
    serializer_class = serializers.NewsSerializer
    queryset = News.objects.select_related("creator", "updater").all()

    def get_object(self):
        return get_object_or_404(News, id=self.request.data.get('id', None))


class ImageUpload(PostCreateView):
    serializer_class = serializers.ImageSerializer
    queryset = Image.objects.all()


class WebNewsList(ListAPIView):
    serializer_class = serializers.WebNewsListSerializer
    queryset = News.objects.prefetch_related('tags').all().distinct().order_by('-id')
    pagination_class = NewsPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        category_key = self.request.query_params.get('cate', 'news')
        tags = Tag.objects.filter(category__key=category_key).all()

        tag_id = self.request.query_params.get('tag')
        if tag_id is not None:
            queryset = queryset.filter(tags__id=tag_id)
        else:
            queryset = queryset.filter(tags__in=tags)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)

        data = {
            "tags": TagNameOnlySerializer(tags, many=True).data,
        }
        response.data.update(data)
        return response


class WebNewsDetail(RetrieveAPIView):
    queryset = News.objects.prefetch_related('tags', 'tags__category').all()
    serializer_class = serializers.WebNewsDetailSerializer