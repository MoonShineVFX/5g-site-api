from django.test import TestCase
from rest_framework.test import APIClient
from django.test.utils import override_settings
from ..shortcuts import debugger_queries
from .models import About, Banner, Partner, Setting
from rest_framework.exceptions import ErrorDetail

from unittest.mock import MagicMock
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from ..tag.tests import setup_category


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
        setup_category()
        About.objects.create(id=1, detail="<html>xxxxxxx</html>")
        Setting.objects.create(id=1, banner_length=5)
        self.b1 = Banner.objects.create(
            id=1, title="title01", image=get_upload_file(file_type='.jpg'), link="company01.com", priority=1, size=0)

        self.p1 = Partner.objects.create(
            id=1, image=get_upload_file(file_type='.jpg'),
            name="夥伴名稱", phone="夥伴電話", email="夥伴信箱", description="夥伴介紹", link="http://google.com.tw", size=0)
        p2 = Partner.objects.create(
            id=2, image=get_upload_file(file_type='.jpg'),
            name="夥伴名稱2", phone="夥伴電話2", email="夥伴信箱2", description="夥伴介紹2", link="http://google.com.tw", size=0)
        self.p1.tags.add(1, 2)
        p2.tags.add(1, 2)

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_get_about(self):
        url = '/api/about'
        response = self.client.post(url)
        assert response.status_code == 200
        assert response.data['detail'] == "<html>xxxxxxx</html>"

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_update_about(self):
        url = '/api/about_update'
        data = {
            "detail": "<html>new</html>",
        }
        response = self.client.post(url, data=data, format='json')
        assert response.status_code == 200
        assert response.data['detail'] == "<html>new</html>"

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_list_banner(self):
        url = '/api/banners'
        response = self.client.post(url)
        print(response.data)
        assert response.status_code == 200

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
        response = self.client.post(url, data=data, format='multipart')
        print(response.data)
        assert response.status_code == 201
        expect_data = {
            'id': 2, 'title': '標題', 'imgUrl': 'banners/test_image_3MFDwfG.jpg', 'link': 'http://google.com.tw',
            'priority': 2}

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
        response = self.client.post(url, data=data, format='json')
        assert response.data == {'result': 1, 'message': '成功', 'errors': [], 'data': {}}
        assert response.status_code == 200
        assert Setting.objects.filter(id=1, banner_length=7).exists()

        data = {
            "length": 1,
        }
        response = self.client.post(url, data=data, format='json')
        assert response.data == {
            'result': 0, 'message': '失敗',
            'errors': [{'non_field_errors': [ErrorDetail(string='length must between 5 and 10', code='invalid')]}],
            'data': {}}
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
        response = self.client.post(url, data=data, format='multipart')
        print(response.data)
        assert response.status_code == 200

        data.pop('tags')
        data.pop('file')
        p = Partner.objects.filter(**data).first()
        assert p is not None
        tag_id_list = [tag.id for tag in p.tags.all()]
        assert tag_id_list == [1]

