from django.test import TestCase
from rest_framework.test import APIClient
from django.test.utils import override_settings
from ..shortcuts import debugger_queries
from .models import Demonstration, Contact, Link, Image
from .models import File as DemoFile
from ..user.models import User

from unittest.mock import MagicMock
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile


def get_upload_file(filename="test", file_type=".zip"):
    file_mock = MagicMock(spec=File, name='FileMock')
    file_mock.name = '{}{}'.format(filename, file_type)
    return file_mock


def get_test_image_file():
    return SimpleUploadedFile(name='test_image.jpg', content=open('./mysite/test.jpeg', 'rb').read(),
                              content_type='image/jpeg')


def get_test_file(**kwargs):
    return get_upload_file(file_type=".rar", **kwargs)


class DemonstrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(id=1, name="user01", email="user01@mail.com")

        c1 = Contact.objects.create(
            name="name", unit="unit", phone="01234567", fax="01234567", email="test@mail.com", creator_id=1)

        self.d1 = Demonstration.objects.create(
            id=1, title="title01", preview=get_upload_file(file_type='.jpg'), contact=c1, type="5g", creator_id=1)
        Demonstration.objects.create(
            id=2, title="title02", preview=get_upload_file(file_type='.jpg'), contact=c1, type="5g", creator_id=1)
        Demonstration.objects.create(
            id=3, title="title03", preview=get_upload_file(file_type='.jpg'), contact=c1, type="tech", creator_id=1)

        Link.objects.create(name="url01", url="http://google.com.tw", demonstration_id=1, creator_id=1)
        Link.objects.create(name="url02", url="http://google.com.tw", demonstration_id=1, creator_id=1)

        Image.objects.create(file=get_upload_file(file_type='.jpg'), size=1, demonstration_id=1, creator_id=1)
        Image.objects.create(file=get_upload_file(file_type='.jpg'), size=1, demonstration_id=1, creator_id=1)

        DemoFile.objects.create(
            file=get_upload_file(file_type='.jpg'), size=1, type="application/pdf", demonstration_id=1, creator_id=1)
        DemoFile.objects.create(
            file=get_upload_file(file_type='.jpg'), size=1, type="application/pdf", demonstration_id=1, creator_id=1)

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_get_web_demo_places_list(self):
        url = '/api/web_demo_places?type=5g'
        response = self.client.get(url)
        print(response.data)
        assert response.status_code == 200

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_get_web_demo_places_detail(self):
        url = '/api/web_demo_places/1'
        response = self.client.get(url)
        print(response.data)
        assert response.status_code == 200