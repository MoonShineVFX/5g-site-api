from .models import About, Banner, Partner, Setting
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..shortcuts import PostUpdateView, WebUpdateView
from . import serializers


class AboutDetail(RetrieveAPIView):
    serializer_class = serializers.AboutSerializer

    def get_object(self):
        return About.objects.first()

    def post(self, request, *args, **kwargs):
        return self.get(self, request, *args, **kwargs)


class AboutUpdate(PostUpdateView):
    serializer_class = serializers.AboutSerializer

    def get_object(self):
        return About.objects.first()


class BannerList(APIView):
    def get(self, request, *args, **kwargs):
        return self.post(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        queryset = Banner.objects.all()
        serializer = serializers.BannerListSerializer(queryset, many=True)
        data = {
            "banner": serializer.data,
            "length": len(serializer.data)
        }
        return Response(data, status=status.HTTP_200_OK)


class BannerLengthSetting(WebUpdateView):
    def get_object(self):
        return Setting.objects.first()

    serializer_class = serializers.BannerLengthSerializer


class BannerCreate(CreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = serializers.BannerCreateUpdateSerializer


class BannerUpdate(GenericAPIView, mixins.UpdateModelMixin):
    queryset = Banner.objects.all()
    serializer_class = serializers.BannerCreateUpdateSerializer

    def get_object(self):
        return get_object_or_404(Banner, id=self.request.data.get('id', None))

    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)