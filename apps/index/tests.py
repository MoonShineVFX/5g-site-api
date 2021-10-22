from django.test import TestCase
from rest_framework.test import APIClient
from django.test.utils import override_settings
from ..shortcuts import debugger_queries
from .models import About, Banner, Partner, Setting
from ..user.models import User
from rest_framework.exceptions import ErrorDetail

from unittest.mock import MagicMock
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from ..tag.tests import setup_categories_tags


def get_upload_file(filename="test", file_type=".zip"):
    file_mock = MagicMock(spec=File, name='FileMock')
    file_mock.name = '{}{}'.format(filename, file_type)
    return file_mock


def get_test_image_file():
    return SimpleUploadedFile(name='test_image.jpg', content=open('./mysite/test.jpeg', 'rb').read(),
                              content_type='image/jpeg')


def get_test_file(**kwargs):
    return get_upload_file(file_type=".rar", **kwargs)


class IndexTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(id=1, name="user01", email="user01@mail.com")
        setup_categories_tags()
        About.objects.create(id=1, detail="<html>xxxxxxx</html>", creator_id=1)
        Setting.objects.create(id=1, banner_length=5, creator_id=1)
        self.b1 = Banner.objects.create(
            id=1, title="title01", image=get_upload_file(file_type='.jpg'), link="company01.com", priority=1, size=0,
            creator_id=1)

        self.p1 = Partner.objects.create(
            id=1, image=get_upload_file(file_type='.jpg'), creator_id=1,
            name="夥伴名稱", phone="夥伴電話", email="夥伴信箱", description="夥伴介紹", link="http://google.com.tw", size=0)
        p2 = Partner.objects.create(
            id=2, image=get_upload_file(file_type='.jpg'), creator_id=1,
            name="夥伴名稱2", phone="夥伴電話2", email="夥伴信箱2", description="夥伴介紹2", link="http://google.com.tw", size=0)
        self.p1.tags.add(1, 2)
        p2.tags.add(1, 2)

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_get_about(self):
        url = '/api/about'
        response = self.client.post(url)
        print(response.data)
        assert response.status_code == 200
        assert response.data['detail'] == "<html>xxxxxxx</html>"

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_update_about(self):
        url = '/api/about_update'
        data = {
            "detail": "<html>new</html>",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='json')
        assert response.status_code == 200
        assert response.data['detail'] == "<html>new</html>"

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_list_banner(self):
        add_list = [
            Banner(
                id=2, title="title02", link="company01.com", priority=3, size=0,
                creator_id=1, created_at="2020-12-01T00:00:00Z", updated_at="2020-12-01"),
            Banner(
                id=3, title="title03", link="company01.com", priority=2, size=0,
                creator_id=1, created_at="2020-02-01T00:00:00Z", updated_at="2020-03-01"),
            Banner(
                id=4, title="title04", link="company01.com", priority=2, size=0,
                creator_id=1, created_at="2020-01-01T00:00:00Z", updated_at="2020-02-01"),
        ]
        Banner.objects.bulk_create(add_list)
        # order: 1 3 4 2
        url = '/api/banners'
        response = self.client.post(url)
        print(response.data)
        assert response.status_code == 200
        expect_order = [1, 3, 4, 2]
        result_ids_order = [b["id"] for b in response.data["banner"]]
        self.assertEqual(result_ids_order, expect_order)

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_create_banner(self):
        url = '/api/banner_create'
        data = {
            "title": "標題",
            "file": get_test_image_file(),
            "link": "http://google.com.tw",
            "priority": 2
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='multipart')
        print(response.data)
        assert response.status_code == 201

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_create_banner_without_file(self):
        url = '/api/banner_create'
        data = {
            "title": "標題",
            "link": "http://google.com.tw",
            "priority": 2
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='json')
        print(response.data)
        assert response.status_code == 201

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_update_banner(self):
        url = '/api/banner_update'
        data = {
            "id": 1,
            "title": "標題",
            "file": get_test_image_file(),
            "link": "http://google.com.tw",
            "priority": 2
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='multipart')
        print(response.data)
        assert response.status_code == 200
        assert Banner.objects.filter(id=1, title="標題", link="http://google.com.tw", priority=2).exists()

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_update_banner_length_setting(self):
        url = '/api/banner_length_setting'
        data = {
            "length": 7,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='json')
        assert response.data == {}
        assert response.status_code == 200
        assert Setting.objects.filter(id=1, banner_length=7).exists()

        data = {
            "length": 1,
        }
        response = self.client.post(url, data=data, format='json')
        assert response.data == {'non_field_errors': [ErrorDetail(string='length must between 5 and 10', code='invalid')]}
        assert response.status_code == 400

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_list_partner(self):
        url = '/api/partners'
        response = self.client.post(url)
        print(response.data)
        assert response.status_code == 200

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_create_partner(self):
        url = '/api/partner_create'
        data = {
            "file": get_test_image_file(),
            "link": "http://google.com.tw",
            "name": "夥伴名稱",
            "phone": "夥伴電話",
            "email": "test@email.com",
            "description": "夥伴介紹",
            "tags": [1, 2]
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='multipart')
        print(response.data)
        assert response.status_code == 201
        data.pop('tags')
        data.pop('file')
        p = Partner.objects.filter(**data).first()
        assert p is not None
        tag_id_list = [tag.id for tag in p.tags.all()]
        assert tag_id_list == [1, 2]

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_update_partner(self):
        url = '/api/partner_update'
        data = {
            "id": 1,
            "file": get_test_image_file(),
            "link": "http://google.com.tw",
            "name": "夥伴名稱",
            "phone": "夥伴電話",
            "email": "test@email.com",
            "description": "夥伴介紹",
            "tags": [1]
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='multipart')
        print(response.data)
        assert response.status_code == 200

        data.pop('tags')
        data.pop('file')
        p = Partner.objects.filter(**data).first()
        assert p is not None
        tag_id_list = [tag.id for tag in p.tags.all()]
        assert tag_id_list == [1]

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_get_web_partner(self):
        url = '/api/web_partners?tag=all'
        response = self.client.get(url)
        print(response.data)
        assert response.data["count"] == 2
        assert response.status_code == 200

        url = '/api/web_partners?tag=tal'
        response = self.client.get(url)
        assert response.data["count"] == 0
        assert response.status_code == 200

        url = '/api/web_partners?tag=1'
        response = self.client.get(url)
        print(response.data)
        assert response.data["count"] == 2
        assert response.status_code == 200

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_get_web_index(self):
        url = '/api/web_index'
        response = self.client.get(url)
        print(response.data)
        assert response.status_code == 200