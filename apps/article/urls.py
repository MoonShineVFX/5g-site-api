from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^news$', views.NewsList.as_view(), name='news-list'),
    url(r'^news/(?P<pk>\d+)$', views.NewsDetail.as_view(), name='news-detail'),
    url(r'^news_create$', views.NewsCreate.as_view(), name='news-create'),
    url(r'^news_update$', views.NewsUpdate.as_view(), name='news-update'),

    url(r'^image_upload$', views.ImageUpload.as_view(), name='image-upload'),

    url(r'^web_news$', views.WebNewsList.as_view(), name='web-news-list'),
    url(r'^web_news/(?P<pk>\d+)$', views.WebNewsDetail.as_view(), name='web-news-detail'),
]