from django.test import TestCase
from ..tag.models import Tag, Category

# Create your tests here.


def setup_category():
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