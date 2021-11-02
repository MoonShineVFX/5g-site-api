from .models import Policy
from ..tag.models import Tag
from . import serializers
from ..tag.serializers import TagNameOnlySerializer
from ..pagination import NewsPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from ..shortcuts import PostCreateView, PostUpdateView


policy_category_dict = {
    'center': 4,
    'local': 5
}


class WebPolicyList(ListAPIView):
    serializer_class = serializers.WebPolicyListSerializer
    queryset = Policy.objects.prefetch_related('tags').all().distinct().order_by('-id')
    pagination_class = NewsPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        category_key = self.request.query_params.get('cate', 'center')
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


class WebPolicyDetail(RetrieveAPIView):
    queryset = Policy.objects.prefetch_related('tags', 'tags__category').all()
    serializer_class = serializers.WebPolicyDetailSerializer


class PolicyList(ListAPIView):
    serializer_class = serializers.PolicyListSerializer
    queryset = Policy.objects.select_related(
        "creator", "updater").prefetch_related("tags", "tags__category").all().distinct().order_by('-id')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {"list": response.data}
        return response


class PolicyDetail(RetrieveAPIView):
    queryset = Policy.objects.select_related("creator", "updater").prefetch_related("tags", "tags__category").all()
    serializer_class = serializers.PolicyDetailSerializer


class PolicyCreate(PostCreateView):
    queryset = Policy.objects.select_related("creator", "updater").prefetch_related("tags").all()
    serializer_class = serializers.PolicyCreateUpdateSerializer


class PolicyUpdate(PostUpdateView):
    queryset = Policy.objects.select_related("creator", "updater").prefetch_related("tags").all()
    serializer_class = serializers.PolicyCreateUpdateSerializer