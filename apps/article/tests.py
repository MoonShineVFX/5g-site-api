from datetime import datetime
from django.test import TestCase
from rest_framework.test import APIClient
from django.test.utils import override_settings
from ..shortcuts import debugger_queries

from .models import News, Image
from ..user.models import User

from ..tag.tests import setup_categories_tags
from ..index.tests import get_test_image_file


class ArticleTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(id=1, name="user01", email="user01@mail.com")
        setup_categories_tags()
        n1 = News.objects.create(id=1, title="news01", description="description", detail="<html>xxxxxxx</html>",
                                 creator_id=1)
        n2 = News.objects.create(id=2, title="news02", description="description", detail="<html>xxxxxxx</html>",
                                 creator_id=1)
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
        assert response.data == {}
        del data["tags"]
        data["creator_id"] = self.user.id
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
        assert response.data == {}
        del data["tags"]
        data["updater_id"] = self.user.id
        news = News.objects.filter(**data).first()
        assert news is not None
        self.assertEqual(news.updated_at.date(), datetime.today().date())
        tag_id_list = [tag.id for tag in news.tags.all()]
        assert tag_id_list == [1, 2]

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_upload_image(self):
        url = '/api/image_upload'
        data = {
            "file": get_test_image_file(),
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='multipart')
        print(response.data)
        assert response.status_code == 201
        assert "imgUrl" in response.data
        img = Image.objects.first()
        assert img is not None
        assert img.size != 0