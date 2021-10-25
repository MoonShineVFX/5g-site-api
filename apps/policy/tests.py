from django.test import TestCase
from rest_framework.test import APIClient
from django.test.utils import override_settings
from ..shortcuts import debugger_queries
from .models import Policy, Contact
from ..user.models import User
from ..tag.tests import setup_categories_tags, Tag


class PolicyTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(id=1, name="user01", email="user01@mail.com")
        setup_categories_tags()

        Tag.objects.create(id=3, name="center_tag", category_id=4, creator_id=self.user.id)
        Tag.objects.create(id=4, name="local_tag", category_id=5, creator_id=self.user.id)

        c1 = Contact.objects.create(
            name="name", unit="unit", phone="01234567", fax="01234567", email="test@mail.com", creator_id=1)

        p1 = Policy.objects.create(
            id=1, title="title01", link="https://www.facebook.com/", contact=c1, creator_id=1)
        p2 = Policy.objects.create(
            id=2, title="title02", link="https://www.facebook.com/", contact=c1, creator_id=1)
        p3 = Policy.objects.create(
            id=3, title="title03", link="https://www.facebook.com/", contact=c1, creator_id=1)

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