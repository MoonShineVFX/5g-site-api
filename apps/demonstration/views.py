from .models import Demonstration
from . import serializers
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView


class WebDemonstrationList(ListAPIView):
    serializer_class = serializers.WebDemonstrationListSerializer
    queryset = Demonstration.objects.all()

    def get_queryset(self):
        type = self.request.query_params.get('type', '5g')
        return self.queryset.filter(type=type)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {"list": response.data}
        return response


class WebDemonstrationDetail(RetrieveAPIView):
    queryset = Demonstration.objects.select_related("contact").prefetch_related('links', 'images', 'files').all()
    serializer_class = serializers.WebDemonstrationDetailSerializer