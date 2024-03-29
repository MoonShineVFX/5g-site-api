from django.db.models.functions import Greatest, Coalesce
from .models import Demonstration, Image, File
from . import serializers
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from ..shortcuts import WebCreateView, WebUpdateView, PostCreateView, PostDestroyView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


class DemonstrationList(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.DemonstrationListSerializer
    queryset = Demonstration.objects.select_related("creator", "updater").annotate(
            latest_time=Coalesce(Greatest('updated_at', 'created_at'), 'created_at')
            ).order_by('-latest_time').all()

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


class DemonstrationDetail(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Demonstration.objects.select_related(
        "creator", "updater").prefetch_related('images', 'files').all()
    serializer_class = serializers.DemonstrationDetailSerializer


class DemonstrationCreate(WebCreateView):
    serializer_class = serializers.DemonstrationCreateUpdateSerializer
    queryset = Demonstration.objects.all()


class DemonstrationUpdate(WebUpdateView):
    serializer_class = serializers.DemonstrationCreateUpdateSerializer
    queryset = Demonstration.objects.all()

    def get_object(self):
        return get_object_or_404(self.queryset, id=self.request.data.get('id', None))


class DemonstrationDelete(PostDestroyView):
    queryset = Demonstration.objects.all()


class ImageUpload(PostCreateView):
    serializer_class = serializers.ImageUploadSerializer
    queryset = Image.objects.all()


class FileUpload(PostCreateView):
    serializer_class = serializers.FileUploadSerializer
    queryset = File.objects.all()


class ImageDelete(PostDestroyView):
    queryset = Image.objects.all()


class FileDelete(PostDestroyView):
    queryset = File.objects.all()


class WebDemonstrationList(ListAPIView):
    serializer_class = serializers.WebDemonstrationListSerializer
    queryset = Demonstration.objects.annotate(
            latest_time=Coalesce(Greatest('updated_at', 'created_at'), 'created_at')
            ).order_by('-latest_time').all()

    def get_queryset(self):
        type = self.request.query_params.get('type', '5g')
        return self.queryset.filter(type=type)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {"list": response.data}
        return response


class WebDemonstrationDetail(RetrieveAPIView):
    queryset = Demonstration.objects.prefetch_related('images', 'files').all()
    serializer_class = serializers.WebDemonstrationDetailSerializer