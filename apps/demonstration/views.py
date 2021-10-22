from .models import Demonstration
from . import serializers
from ..pagination import NewsPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView


class WebDemonstrationList(ListAPIView):
    serializer_class = serializers.WebDemonstrationListSerializer
    queryset = Demonstration.objects.all()

    def get_queryset(self):
        type = self.request.query_params.get('type', '5g')
        return self.queryset.filter(type=type)


class WebDemonstrationDetail(RetrieveAPIView):
    queryset = Demonstration.objects.select_related("contact").prefetch_related('links', 'images', 'files').all()
    serializer_class = serializers.WebDemonstrationDetailSerializer