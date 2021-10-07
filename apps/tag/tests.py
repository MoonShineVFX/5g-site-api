from django.test import TestCase
from rest_framework.test import APIClient
from django.test.utils import override_settings
from ..shortcuts import debugger_queries
from .models import Tag, Category
from ..user.models import User


def setup_categories_tags(creator_id=1):
    cats = [
        Category(**{"id": 1, "key": "news", "name": "新聞快訊"}),
        Category(**{"id": 2, "key": "newsIndustry", "name": "產業訊息"}),
        Category(**{"id": 3, "key": "partner", "name": "合作夥伴"}),
        Category(**{"id": 4, "key": "center", "name": "中央資源"}),
        Category(**{"id": 5, "key": "local", "name": "地方資源"}),
    ]
    Category.objects.bulk_create(cats)

    Tag.objects.create(id=1, name="互動", category_id=1, creator_id=creator_id)
    Tag.objects.create(id=2, name="5G", category_id=2, creator_id=creator_id)


class TagTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(id=1, name="user01", email="user01@mail.com")
        setup_categories_tags()

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
            "tags": [
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
        self.client.force_authenticate(user=self.user)
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
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='json')
        assert response.status_code == 200
        print(response.data)
        self.assertEqual(
            response.data,
            {'id': 1, 'name': '新名稱', 'categoryId': 2, 'categoryKey': 'newsIndustry', 'categoryName': '產業訊息'})
        assert Tag.objects.filter(id=1, name="新名稱", category_id=2).exists()

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_common(self):
        url = '/api/common'
        data = {
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='json')
        assert response.status_code == 200

        expect = {
                'userId': 1,
                'userName': 'user01',
                'newsTags': [
                    {'id': 1,
                     'name': '互動',
                     'categoryId': 1,
                     'categoryKey': 'news',
                     'categoryName': '新聞快訊'},
                    {'id': 2,
                     'name': '5G',
                     'categoryId': 2,
                     'categoryKey': 'newsIndustry',
                     'categoryName': '產業訊息'}
                ]}
        assert response.data == expect
