from .models import About, Privacy, Security, Banner, Partner, Setting
from ..article.models import News
from ..tag.models import Tag
from ..demonstration.models import Demonstration
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ..shortcuts import PostCreateView, PostUpdateView, WebUpdateView
from ..pagination import PartnerPagination
from . import serializers
from ..tag.serializers import TagNameOnlySerializer
from ..demonstration.serializers import WebDemonstrationListSerializer
from rest_framework.permissions import IsAuthenticated


class AboutDetail(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.AboutSerializer

    def get_object(self):
        return About.objects.select_related("creator", "updater").first()

    def post(self, request, *args, **kwargs):
        return self.get(self, request, *args, **kwargs)


class WebAboutDetail(RetrieveAPIView):
    serializer_class = serializers.WebAboutSerializer

    def get_object(self):
        return About.objects.first()


class AboutUpdate(PostUpdateView):
    serializer_class = serializers.AboutSerializer

    def get_object(self):
        return About.objects.select_related("creator", "updater").first()


class PrivacyDetail(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.PrivacySerializer

    def get_object(self):
        return Privacy.objects.select_related("creator", "updater").first()

    def post(self, request, *args, **kwargs):
        return self.get(self, request, *args, **kwargs)


class WebPrivacyDetail(RetrieveAPIView):
    serializer_class = serializers.WebPrivacySerializer

    def get_object(self):
        return Privacy.objects.first()


class PrivacyUpdate(PostUpdateView):
    serializer_class = serializers.PrivacySerializer

    def get_object(self):
        return Privacy.objects.select_related("creator", "updater").first()


class SecurityDetail(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.SecuritySerializer

    def get_object(self):
        return Security.objects.select_related("creator", "updater").first()

    def post(self, request, *args, **kwargs):
        return self.get(self, request, *args, **kwargs)


class WebSecurityDetail(RetrieveAPIView):
    serializer_class = serializers.WebSecuritySerializer

    def get_object(self):
        return Security.objects.first()


class SecurityUpdate(PostUpdateView):
    serializer_class = serializers.SecuritySerializer

    def get_object(self):
        return Security.objects.select_related("creator", "updater").first()


class BannerList(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        return self.post(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        queryset = Banner.objects.select_related("creator", "updater").order_by("priority", "-updated_at", "-created_at").all()
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


class BannerCreate(PostCreateView):
    queryset = Banner.objects.select_related("creator", "updater").all()
    serializer_class = serializers.BannerCreateUpdateSerializer


class BannerUpdate(PostUpdateView):
    queryset = Banner.objects.select_related("creator", "updater").all()
    serializer_class = serializers.BannerCreateUpdateSerializer


class PartnerList(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        return self.post(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        partners = Partner.objects.select_related("creator", "updater").prefetch_related('tags').all()
        partner_tags = Tag.objects.filter(category_id=3)

        data = {
            "tags": TagNameOnlySerializer(partner_tags, many=True).data,
            "partners": serializers.PartnerSerializer(partners, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)


class PartnerCreate(PostCreateView):
    queryset = Partner.objects.select_related("creator", "updater").prefetch_related('tags').all()
    serializer_class = serializers.PartnerCreateUpdateSerializer


class PartnerUpdate(PostUpdateView):
    queryset = Partner.objects.select_related("creator", "updater").prefetch_related('tags').all()
    serializer_class = serializers.PartnerCreateUpdateSerializer


class WebPartnerList(ListAPIView):
    serializer_class = serializers.WebPartnerSerializer
    queryset = Partner.objects.all()
    pagination_class = PartnerPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        tag_key = self.request.query_params.get('tag', 'all')
        if tag_key == 'all':
            pass
        else:
            try:
                int(tag_key)
                queryset = queryset.filter(tags__id=tag_key)
            except ValueError:
                queryset = queryset.none()

        page = self.paginate_queryset(queryset.distinct().order_by('-id'))
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)

        partner_tags = Tag.objects.filter(category_id=3)
        data = {
            "tags": TagNameOnlySerializer(partner_tags, many=True).data,
        }
        response.data.update(data)
        return response


class WebIndexList(APIView):
    def get(self, request, *args, **kwargs):
        setting = Setting.objects.first()
        banners = Banner.objects.select_related("creator", "updater").order_by(
            "priority", "-updated_at", "-created_at").all()[:setting.banner_length]
        news = News.objects.filter(tags__category_id=1).order_by("-hot_at", "-created_at").distinct()[:3]
        news_industries = News.objects.filter(tags__category_id=2).order_by("-hot_at", "-created_at").distinct()[:3]
        partner_tags = Tag.objects.filter(category_id=3)
        demo_places = Demonstration.objects.order_by("-updated_at", "-created_at").all()[:3]

        data = {
            "banners": serializers.WebIndexBannerSerializer(banners, many=True).data,
            "demoPlaces": WebDemonstrationListSerializer(demo_places, many=True).data,
            "news": {
                "news": serializers.WebIndexNewsSerializer(news, many=True).data,
                "newsIndustries": serializers.WebIndexNewsSerializer(news_industries, many=True).data,
            },
            "partnerTags": TagNameOnlySerializer(partner_tags, many=True).data
        }
        return Response(data, status=status.HTTP_200_OK)