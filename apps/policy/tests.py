from django.test import TestCase
from rest_framework.test import APIClient
from django.test.utils import override_settings
from ..shortcuts import debugger_queries
from .models import Policy
from ..user.models import User
from ..tag.tests import setup_categories_tags, Tag


class PolicyTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(id=1, name="user01", email="user01@mail.com")
        setup_categories_tags()

        Tag.objects.create(id=3, name="center_tag", category_id=4, creator_id=self.user.id)
        Tag.objects.create(id=4, name="local_tag", category_id=5, creator_id=self.user.id)

        p1 = Policy.objects.create(
            id=1, title="title01", link="https://www.facebook.com/", creator_id=1)
        p2 = Policy.objects.create(
            id=2, title="title02", link="https://www.facebook.com/", creator_id=1)
        p3 = Policy.objects.create(
            id=3, title="title03", link="https://www.facebook.com/", creator_id=1)

        p1.tags.add(3)

        p2.tags.add(4)
        p3.tags.add(4)

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_get_web_policy_list(self):
        url = '/api/web_policies?cate=local'
        response = self.client.get(url)
        print(response.data)
        assert response.status_code == 200

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_get_web_policy_detail(self):
        url = '/api/web_policies/1'
        response = self.client.get(url)
        print(response.data)
        assert response.status_code == 200

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_get_policy_list(self):
        url = '/api/policies?cate=local'
        response = self.client.get(url)
        print(response.data)
        assert response.status_code == 200

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_get_policy_detail(self):
        url = '/api/policies/1'
        response = self.client.get(url)
        print(response.data)
        assert response.status_code == 200

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_policy_create(self):
        url = '/api/policy_create'
        data = {
            "title": "標題",
            "titleSecondary": "次標題",
            "description": "介紹",
            "tags": [1],
            "contactUnit": "中華民國創業投資商業同業公會",
            "contactName": "曾炫誠",
            "contactPhone": "(02)2546-5336",
            "contactFax": "(02)2389-0636",
            "contactEmail": "owen.tzeng@tvca.org.tw",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format="json")
        print(response.data)
        assert response.status_code == 201
        assert Policy.objects.filter(title=data["title"], creator_id=self.user.id).exists()

    @override_settings(DEBUG=True)
    @debugger_queries
    def test_policy_update(self):
        url = '/api/policy_update'
        data = {
            "id": 1,
            "title": "標題",
            "titleSecondary": "次標題",
            "description": "介紹",
            "tags": [1],
            "contactUnit": "中華民國創業投資商業同業公會",
            "contactName": "曾炫誠",
            "contactPhone": "(02)2546-5336",
            "contactFax": "(02)2389-0636",
            "contactEmail": "owen.tzeng@tvca.org.tw",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format="json")
        print(response.data)
        assert response.status_code == 200
        assert Policy.objects.filter(id=1, title=data["title"], updater_id=self.user.id).exists()