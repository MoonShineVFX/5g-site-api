from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^web_policies$', views.WebPolicyList.as_view(), name='web-policy-list'),
    url(r'^web_policies/(?P<pk>\d+)$', views.WebPolicyDetail.as_view(), name='web-policy-detail'),
]