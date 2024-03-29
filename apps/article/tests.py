from datetime import datetime
from django.test import TestCase
from rest_framework.test import APIClient
from django.test.utils import override_settings
from ..shortcuts import debugger_queries

from .models import News, Image
from ..user.models import User
from ..tag.models import Tag

from ..tag.tests import setup_categories_tags
from ..index.tests import get_test_image_file


class ArticleTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(id=1, name="user01", email="user01@mail.com")
        setup_categories_tags()
        n1 = News.objects.create(id=1, title="news01", description="description", detail="<html>xxxxxxx</html>",
                                 creator_id=1, is_hot=True, hot_at="2020-01-01 00:00:00")
        n2 = News.objects.create(id=2, title="news02", description="description", detail="<html>xxxxxxx</html>",
                                 creator_id=1)
        n1.tags.add(1)
        n2.tags.add(2)

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_get_news_list(self):
        url = '/api/news'
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        print(response)
        assert response.status_code == 200
        print(response.data['list'])
        assert len(response.data['list']) == 2

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_get_news_list_with_is_active_false(self):
        News.objects.filter(id=1).update(is_active=False)
        url = '/api/news'
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        print(response)
        assert response.status_code == 200
        assert len(response.data['list']) == 2

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_news_detail(self):
        url = '/api/news/1'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        print(response.data)
        assert response.status_code == 200

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_create_news(self):
        url = '/api/news_create'
        data = {
            "title": "new title",
            "description": "description",
            "detail": "<html>news</html>",
            "isHot": True,
            "tags": [1, 2]
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='json')
        assert response.status_code == 201
        assert response.data == {}
        del data["tags"]
        del data["isHot"]
        data["is_hot"] = True
        data["creator_id"] = self.user.id
        news = News.objects.filter(**data).first()
        assert news is not None
        assert news.hot_at is not None
        tag_id_list = [tag.id for tag in news.tags.all()]
        assert tag_id_list == [1, 2]

        data = {
            "length": 1,
        }
        response = self.client.post(url, data=data, format='json')
        assert response.status_code == 400

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_create_news_blank(self):
        url = '/api/news_create'
        data = {
            "title": "",
            "description": "",
            "detail": "",
            "isHot": False,
            "tags": [1, 2]
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='json')
        assert response.status_code == 201

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_update_news(self):
        url = '/api/news_update'
        data = {
            "id": 1,
            "title": "new title",
            "description": "description",
            "detail": "<html>news</html>",
            "isHot": False,
            "isActive": False,
            "tags": [1, 2]
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='json')
        assert response.status_code == 200
        assert response.data == {}
        del data["tags"]
        del data["isHot"]
        del data["isActive"]
        data["is_hot"] = False
        data["is_active"] = False
        data["hot_at"] = None
        data["updater_id"] = self.user.id
        news = News.objects.filter(**data).first()
        assert news is not None
        self.assertEqual(news.updated_at.date(), datetime.today().date())
        tag_id_list = [tag.id for tag in news.tags.all()]
        assert tag_id_list == [1, 2]

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_delete_news(self):
        url = '/api/news_delete'
        data = {
            "id": 1,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='json')
        print(response.status_code)
        assert response.status_code == 200
        assert not News.objects.filter(id=1).exists()

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


class WebArticleTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(id=1, name="user01", email="user01@mail.com")
        setup_categories_tags()
        Tag.objects.create(id=3, name="tag3", category_id=1, creator_id=self.user.id)

        Tag.objects.create(id=4, name="tag4", category_id=2, creator_id=self.user.id)
        Tag.objects.create(id=5, name="tag5", category_id=2, creator_id=self.user.id)

        n1 = News.objects.create(id=1, title="news01", description="description", detail="<html>xxxxxxx</html>",
                                 creator_id=1, is_hot=True, hot_at="2020-01-01 00:00:00")
        n2 = News.objects.create(id=2, title="news02", description="description", detail="<html>xxxxxxx</html>",
                                 creator_id=1)
        n3 = News.objects.create(id=3, title="news03", description="description", detail="<html>xxxxxxx</html>",
                                 creator_id=1)
        n1.tags.add(1, 3)
        n2.tags.add(2, 4)
        n3.tags.add(1)

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_get_web_news_order(self):
        n2 = News.objects.get(id=2)
        n2.tags.add(1)

        News.objects.filter(id=1).update(created_at="2020-01-01 00:00:00", updated_at="2020-12-01 00:00:00")
        News.objects.filter(id=2).update(created_at="2020-03-01 00:00:00", )
        News.objects.filter(id=3).update(created_at="2020-04-01 00:00:00", )
        url = '/api/web_news'
        response = self.client.get(url)
        print(response.data)
        assert response.status_code == 200
        result_list = [item["id"] for item in response.data["list"]]
        assert result_list == [1, 3, 2]

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_get_web_news_list(self):
        url = '/api/web_news?cate=newsIndustry'
        response = self.client.get(url)
        print(response.data)
        assert response.status_code == 200

        url = '/api/web_news?cate=newsIndustry&tag=5'
        response = self.client.get(url)
        print(response.data)
        assert response.status_code == 200
        assert response.data['list'] == []

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_get_web_news_list_with_is_active_false(self):
        News.objects.filter(id=1).update(is_active=False)
        url = '/api/web_news'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        print(response)
        assert response.status_code == 200
        assert len(response.data['list']) == 1

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_get_web_news_detail(self):
        url = '/api/web_news/2'
        response = self.client.get(url)
        print(response.data)
        assert response.status_code == 200
        assert response.data['otherNews'] == []

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_get_web_news_detail_with_end(self):
        url = '/api/web_news/3'
        response = self.client.get(url)
        print(response.data)
        assert response.status_code == 200
        assert response.data['otherNews'][0]["id"] == 1
        assert len(response.data['otherNews']) == 1