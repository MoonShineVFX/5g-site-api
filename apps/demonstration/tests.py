from django.test import TestCase
from rest_framework.test import APIClient
from django.test.utils import override_settings
from ..shortcuts import debugger_queries
from .models import Demonstration, Image
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

        self.d1 = Demonstration.objects.create(
            id=1, title="title01", thumb=get_upload_file(file_type='.jpg'), type="5g", creator_id=1)
        Demonstration.objects.create(
            id=2, title="title02", thumb=get_upload_file(file_type='.jpg'), type="5g", creator_id=1)
        Demonstration.objects.create(
            id=3, title="title03", thumb=get_upload_file(file_type='.jpg'), type="tech", creator_id=1)

        Image.objects.create(id=1, file=get_upload_file(file_type='.jpg'), size=1, demonstration_id=1, creator_id=1)
        Image.objects.create(id=2, file=get_upload_file(file_type='.jpg'), size=1, demonstration_id=1, creator_id=1)

        DemoFile.objects.create(id=1,
            file=get_upload_file(file_type='.jpg'), size=1, type="application/pdf", demonstration_id=1, creator_id=1)
        DemoFile.objects.create(id=2,
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

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_get_demo_places_list(self):
        url = '/api/demo_places'
        response = self.client.get(url)
        print(response.data)
        assert response.status_code == 200

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_get_demo_places_detail(self):
        url = '/api/demo_places/1'
        response = self.client.get(url)
        print(response.data)
        assert response.status_code == 200

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_demo_places_create(self):
        url = '/api/demo_place_create'
        data = {
            "title": "駁二大義區C7動漫倉庫",
            "address": "台北市南港區忠孝東路四段",
            #"locationUrl": "https://www.google.com.tw/maps/place/%E5%A4%A2%E6%83%B3%E5%8B%95%E7%95%AB/@25.0510988,121.5928083,17z/data=!3m2!4b1!5s0x3442ab6558ba3521:0xbe34660725096e72!4m5!3m4!1s0x3442aba32bd21781:0x592cb0b7781a69d3!8m2!3d25.051094!4d121.594997",
            #"description": "PAIR位於大義區C9倉庫，有8間10坪的駐村藝術家創作工作室。",
            "websiteName": "駁二共創基地網",
            "websiteUrl": "https://beboss.wda.gov.tw",
            "type": "5g",
            "contactUnit": "中華民國創業投資商業同業公會",
            "contactName": "曾炫誠",
            "contactPhone": "(02)2546-5336",
            "contactFax": "(02)2389-0636",
            "contactEmail": "owen.tzeng@tvca.org.tw",
            #"videoIframe": "videoIframe",
            "thumb": get_test_image_file(),
            "byMRT": "",
            "byDrive": ""

        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='multipart')
        print(response.data)
        assert response.status_code == 201
        assert Demonstration.objects.filter(title=data["title"], creator_id=self.user.id).exists()

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_demo_places_update(self):
        url = '/api/demo_place_update'
        data = {
            "id": 1,
            "title": "駁二大義區C7動漫倉庫",
            "address": "台北市南港區忠孝東路四段",
            #"locationUrl": "https://www.google.com.tw/maps/place/%E5%A4%A2%E6%83%B3%E5%8B%95%E7%95%AB/@25.0510988,121.5928083,17z/data=!3m2!4b1!5s0x3442ab6558ba3521:0xbe34660725096e72!4m5!3m4!1s0x3442aba32bd21781:0x592cb0b7781a69d3!8m2!3d25.051094!4d121.594997",
            #"description": "PAIR位於大義區C9倉庫，有8間10坪的駐村藝術家創作工作室。",
            "websiteName": "駁二共創基地網",
            "websiteUrl": "https://beboss.wda.gov.tw",
            "type": "5g",
            "contactUnit": "中華民國創業投資商業同業公會",
            "contactName": "曾炫誠",
            "contactPhone": "(02)2546-5336",
            "contactFax": "(02)2389-0636",
            "contactEmail": "owen.tzeng@tvca.org.tw",
            #"videoIframe": "videoIframe",
            "thumb": get_test_image_file(),
            "byMRT": "",
            "byDrive": ""

        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='multipart')
        print(response.data)
        assert response.status_code == 200
        assert Demonstration.objects.filter(title=data["title"], updater_id=self.user.id).exists()

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_upload_image(self):
        url = '/api/demo_place_image_upload'
        data = {
            "demoPlaceId": 1,
            "file": get_test_image_file(),
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='multipart')
        print(response.data)
        assert response.status_code == 201
        assert "imgUrl" in response.data
        img = Image.objects.filter(id=response.data["id"], demonstration_id=1)[0]
        assert img is not None
        assert img.size != 0

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_upload_file(self):
        url = '/api/demo_place_file_upload'
        data = {
            "demoPlaceId": 1,
            "file": get_test_image_file(),
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='multipart')
        print(response.data)
        assert response.status_code == 201
        assert "url" in response.data
        upload_file = DemoFile.objects.filter(id=response.data["id"], demonstration_id=1)[0]
        assert upload_file is not None
        assert upload_file.size != 0