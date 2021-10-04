from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^news$', views.NewsList.as_view(), name='news-list'),
    url(r'^news/(?P<pk>\d+)$', views.NewsDetail.as_view(), name='news-detail'),
    url(r'^news_create$', views.NewsCreate.as_view(), name='news-create'),
    url(r'^news_update$', views.NewsUpdate.as_view(), name='news-update'),

]