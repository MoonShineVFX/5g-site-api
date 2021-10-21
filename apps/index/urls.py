from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^banners$', views.BannerList.as_view(), name='banner-list'),
    url(r'^banner_create$', views.BannerCreate.as_view(), name='banner-create'),
    url(r'^banner_update$', views.BannerUpdate.as_view(), name='banner-update'),
    url(r'^banner_length_setting$', views.BannerLengthSetting.as_view(), name='banner-length-setting'),

    url(r'^about$', views.AboutDetail.as_view(), name='about-detail'),
    url(r'^about_update$', views.AboutUpdate.as_view(), name='about-update'),

    url(r'^partners$', views.PartnerList.as_view(), name='partner-list'),
    url(r'^partner_create$', views.PartnerCreate.as_view(), name='partner-create'),
    url(r'^partner_update$', views.PartnerUpdate.as_view(), name='partner-update'),

    url(r'^web_partners$', views.WebPartnerList.as_view(), name='web-partner-list'),
]