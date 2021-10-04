from django.test import TestCase
from rest_framework.test import APIClient
from django.test.utils import override_settings
from ..shortcuts import debugger_queries
from .models import Tag, Category

from collections import OrderedDict

def setup_category():
    cats = [
        Category(**{"id": 1, "key": "news", "name": "新聞快訊"}),
        Category(**{"id": 2, "key": "newsIndustry", "name": "產業訊息"}),
        Category(**{"id": 3, "key": "partner", "name": "合作夥伴"}),
        Category(**{"id": 4, "key": "center", "name": "中央資源"}),
        Category(**{"id": 5, "key": "local", "name": "地方資源"}),
    ]
    Category.objects.bulk_create(cats)

    Tag.objects.create(id=1, name="互動", category_id=1)
    Tag.objects.create(id=2, name="5G", category_id=2)


class TagTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        setup_category()

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_get_tags_and_categories(self):
        url = '/api/tags_and_categories'
        response = self.client.post(url)
        print(response.data)
        assert response.status_code == 200

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_tag_create(self):
        url = '/api/tag_create'
        data = {
            "tag": [
                {
                    "name": "互動2",
                    "categoryId": 1
                },
                {
                    "name": "5G2",
                    "categoryId": 2
                }
            ]
        }
        response = self.client.post(url, data=data, format='json')
        assert response.status_code == 201
        print(response.data)
        assert Tag.objects.filter(name="互動2", category_id=1).exists()
        assert Tag.objects.filter(name="5G2", category_id=2).exists()

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_tag_create(self):
        url = '/api/tag_create'
        data = {
            "tag": [
                {
                    "name": "互動2",
                    "categoryId": 1
                },
                {
                    "name": "5G2",
                    "categoryId": 2
                }
            ]
        }
        response = self.client.post(url, data=data, format='json')
        assert response.status_code == 201
        print(response.data)
        assert Tag.objects.filter(name="互動2", category_id=1).exists()
        assert Tag.objects.filter(name="5G2", category_id=2).exists()

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_tag_update(self):
        url = '/api/tag_update'
        data = {
            "id": 1,
            "name": "新名稱",
            "categoryId": 2
        }
        response = self.client.post(url, data=data, format='json')
        assert response.status_code == 200
        assert response.data == {'id': 1, 'name': '新名稱', 'category': 'newsIndustry', 'categoryName': '產業訊息'}
        assert Tag.objects.filter(id=1, name="新名稱", category_id=2).exists()