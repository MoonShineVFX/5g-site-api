from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Tag, Category
from . import serializers
from ..shortcuts import PostUpdateView, PostDestroyView
from rest_framework.permissions import IsAuthenticated


class CommonView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        news_tags = Tag.objects.select_related("creator", "updater", "category").filter(category_id__in=[1, 2])
        policy_tags = Tag.objects.select_related("creator", "updater", "category").filter(category_id__in=[4, 5])

        data = {
            "userId": self.request.user.id,
            "userName": self.request.user.name,
            "newsTags": serializers.TagWithCategorySerializer(news_tags, many=True).data,
            "policyTags": serializers.TagWithCategorySerializer(policy_tags, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)


class TagAndCategoryList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.post(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        tags = Tag.objects.select_related("creator", "updater", "category").all()
        categories = Category.objects.all()

        data = {
            "tags": serializers.TagWithCategorySerializer(tags, many=True).data,
            "categories": serializers.CategorySerializer(categories, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)


class TagCreate(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        serializer = serializers.TagListCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator_id=self.request.user.id)

            tags = Tag.objects.select_related("creator", "updater", "category").all()
            data = {
                "tags": serializers.TagWithCategorySerializer(tags, many=True).data,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagUpdate(PostUpdateView):
    queryset = Tag.objects.select_related("creator", "updater").all()
    serializer_class = serializers.TagUpdateSerializer


class TagDelete(PostDestroyView):
    queryset = Tag.objects.select_related("creator", "updater").all()