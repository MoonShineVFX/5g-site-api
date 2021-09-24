from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^banners$', views.BannerList.as_view(), name='banner-list'),
    url(r'^banner_create$', views.BannerCreate.as_view(), name='banner-create'),
    url(r'^banner_update$', views.BannerUpdate.as_view(), name='banner-update'),
    url(r'^banner_length_setting$', views.BannerLengthSetting.as_view(), name='banner-length-setting'),
]