from .models import About, Banner, Partner, Setting
from ..tag.models import Tag
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..shortcuts import PostUpdateView, WebUpdateView
from . import serializers
from ..tag.serializers import TagSerializer


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


class BannerUpdate(PostUpdateView):
    queryset = Banner.objects.all()
    serializer_class = serializers.BannerCreateUpdateSerializer


class PartnerList(APIView):
    def get(self, request, *args, **kwargs):
        return self.post(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        partners = Partner.objects.prefetch_related('tags').all()
        tags = Tag.objects.all()

        data = {
            "tag": TagSerializer(tags, many=True).data,
            "partner": serializers.PartnerSerializer(partners, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)


class PartnerCreate(CreateAPIView):
    queryset = Partner.objects.all()
    serializer_class = serializers.PartnerCreateUpdateSerializer


class PartnerUpdate(PostUpdateView):
    queryset = Partner.objects.all()
    serializer_class = serializers.PartnerCreateUpdateSerializer
