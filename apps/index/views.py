from .models import Banner, Partner
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from . import serializers


res_success = {
    "result": 1,
    "message": "",
    "data": {}
}
res_error = {
    "result": 0,
    "message": "",
    "errors": [],
}


class BannerList(APIView):
    def post(self, request, *args, **kwargs):
        queryset = Banner.objects.all()
        serializer = serializers.BannerListSerializer(queryset, many=True)
        data = {
            "banner": serializer.data,
            "length": len(serializer.data)
        }
        return Response(data, status=status.HTTP_200_OK)


class BannerLengthSetting(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.BannerLengthSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "result": 1,
                "message": "成功",
                "errors": [],
                "data": {}
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                "result": 0,
                "message": "失敗",
                "errors": [serializer.errors],
                "data": {}
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class BannerCreate(CreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = serializers.BannerCreateUpdateSerializer


class BannerUpdate(UpdateAPIView):
    queryset = Banner.objects.all()
    serializer_class = serializers.BannerCreateUpdateSerializer

    def get_object(self):
        return get_object_or_404(Banner, id=self.request.data.get('id', None))

    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)