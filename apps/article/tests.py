from django.test import TestCase
from rest_framework.test import APIClient
from django.test.utils import override_settings
from ..shortcuts import debugger_queries
from rest_framework.exceptions import ErrorDetail

from .models import News
from ..user.models import User
from ..tag.models import Tag, Category


class ArticleTest(TestCase):
    def setup_category(self):
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

    def setUp(self):
        self.client = APIClient()
        self.setup_category()
        self.user = User.objects.create(id=1, name="user01", email="user01@mail.com")
        n1 = News.objects.create(id=1, title="news01", description="description", detail="<html>xxxxxxx</html>",
                                 author_id=1)
        n2 = News.objects.create(id=2, title="news02", description="description", detail="<html>xxxxxxx</html>",
                                 author_id=1)
        n1.tags.add(1)
        n2.tags.add(2)

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_get_news_list(self):
        url = '/api/news'
        response = self.client.post(url)
        print(response)
        assert response.status_code == 200
        print(response.data['list'])

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_news_detail(self):
        url = '/api/news/1'
        response = self.client.get(url)
        assert response.data == {
            'id': 1, 'title': 'news01', 'description': 'description', 'detail': '<html>xxxxxxx</html>', 'tags': [1]}

        assert response.status_code == 200

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_create_news(self):
        url = '/api/news_create'
        data = {
            "title": "new title",
            "description": "description",
            "detail": "<html>news</html>",
            "tags": [1, 2]
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='json')
        assert response.status_code == 201
        assert response.data == {'result': 1, 'message': '成功', 'errors': [], 'data': {}}
        del data["tags"]

        news = News.objects.filter(**data).first()
        assert news is not None
        tag_id_list = [tag.id for tag in news.tags.all()]
        assert tag_id_list == [1, 2]

        data = {
            "length": 1,
        }
        response = self.client.post(url, data=data, format='json')
        assert response.status_code == 400

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_update_news(self):
        url = '/api/news_update'
        data = {
            "id": 1,
            "title": "new title",
            "description": "description",
            "detail": "<html>news</html>",
            "tags": [1, 2]
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='json')
        assert response.status_code == 200
        assert response.data == {'result': 1, 'message': '成功', 'errors': [], 'data': {}}
        del data["tags"]
        news = News.objects.filter(**data).first()
        assert news is not None
        tag_id_list = [tag.id for tag in news.tags.all()]
        assert tag_id_list == [1, 2]