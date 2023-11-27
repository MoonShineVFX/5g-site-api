from django.db.models.functions import Greatest, Coalesce
from .models import Policy
from ..tag.models import Tag
from . import serializers
from ..tag.serializers import TagNameOnlySerializer
from ..pagination import NewsPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from ..shortcuts import PostCreateView, PostUpdateView, PostDestroyView
from rest_framework.permissions import IsAuthenticated


policy_category_dict = {
    'center': 4,
    'local': 5
}


class WebPolicyList(ListAPIView):
    serializer_class = serializers.WebPolicyListSerializer
    queryset = Policy.objects.prefetch_related('tags').distinct().annotate(
            latest_time=Coalesce(Greatest('updated_at', 'created_at'), 'created_at')
            ).order_by('-latest_time').all()
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
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.PolicyListSerializer
    queryset = Policy.objects.select_related(
        "creator", "updater").prefetch_related("tags", "tags__category").distinct().annotate(
            latest_time=Coalesce(Greatest('updated_at', 'created_at'), 'created_at')
            ).order_by('-latest_time').all()

    def post(self, request, *args, **kwargs):
        return self.get(self, request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {"list": response.data}
        return response


class PolicyDetail(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Policy.objects.select_related("creator", "updater").prefetch_related("tags", "tags__category").all()
    serializer_class = serializers.PolicyDetailSerializer


class PolicyCreate(PostCreateView):
    queryset = Policy.objects.select_related("creator", "updater").prefetch_related("tags").all()
    serializer_class = serializers.PolicyCreateUpdateSerializer


class PolicyUpdate(PostUpdateView):
    queryset = Policy.objects.select_related("creator", "updater").prefetch_related("tags").all()
    serializer_class = serializers.PolicyCreateUpdateSerializer


class PolicyDelete(PostDestroyView):
    queryset = Policy.objects.select_related("creator", "updater").prefetch_related("tags").all()