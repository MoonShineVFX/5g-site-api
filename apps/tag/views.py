from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Tag, Category
from . import serializers
from ..shortcuts import PostUpdateView


class TagAndCategoryList(APIView):
    def get(self, request, *args, **kwargs):
        return self.post(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        tags = Tag.objects.select_related('category').all()
        categories = Category.objects.all()

        data = {
            "tag": serializers.TagWithCategorySerializer(tags, many=True).data,
            "category": serializers.CategorySerializer(categories, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)


class TagCreate(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.TagListCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            tags = Tag.objects.select_related('category').all()
            data = {
                "tag": serializers.TagWithCategorySerializer(tags, many=True).data,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagUpdate(PostUpdateView):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagUpdateSerializer