from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^banners$', views.BannerList.as_view(), name='banner-list'),
    url(r'^banner_create$', views.BannerCreate.as_view(), name='banner-create'),
    url(r'^banner_update$', views.BannerUpdate.as_view(), name='banner-update'),
    url(r'^banner_delete$', views.BannerDelete.as_view(), name='banner-delete'),

    url(r'^banner_length_setting$', views.BannerLengthSetting.as_view(), name='banner-length-setting'),

    url(r'^about$', views.AboutDetail.as_view(), name='about-detail'),
    url(r'^about_update$', views.AboutUpdate.as_view(), name='about-update'),

    url(r'^privacy$', views.PrivacyDetail.as_view(), name='privacy-detail'),
    url(r'^privacy_update$', views.PrivacyUpdate.as_view(), name='privacy-update'),

    url(r'^security$', views.SecurityDetail.as_view(), name='security-detail'),
    url(r'^security_update$', views.SecurityUpdate.as_view(), name='security-update'),

    url(r'^partners$', views.PartnerList.as_view(), name='partner-list'),
    url(r'^partner_create$', views.PartnerCreate.as_view(), name='partner-create'),
    url(r'^partner_update$', views.PartnerUpdate.as_view(), name='partner-update'),
    url(r'^partner_delete$', views.PartnerDelete.as_view(), name='partner-delete'),

    url(r'^web_partners$', views.WebPartnerList.as_view(), name='web-partner-list'),

    url(r'^web_about$', views.WebAboutDetail.as_view(), name='web-about'),
    url(r'^web_privacy$', views.WebPrivacyDetail.as_view(), name='web-privacy-detail'),
    url(r'^web_security$', views.WebSecurityDetail.as_view(), name='web-security-detail'),

    url(r'^web_index$', views.WebIndexList.as_view(), name='web-index'),
]