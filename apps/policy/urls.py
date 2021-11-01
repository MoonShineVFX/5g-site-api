from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^web_policies$', views.WebPolicyList.as_view(), name='web-policy-list'),
    url(r'^web_policies/(?P<pk>\d+)$', views.WebPolicyDetail.as_view(), name='web-policy-detail'),

    url(r'^policies$', views.PolicyList.as_view(), name='policy-list'),
    url(r'^policies/(?P<pk>\d+)$', views.PolicyDetail.as_view(), name='policy-detail'),
    url(r'^policy_create$', views.PolicyCreate.as_view(), name='policy-create'),
    url(r'^policy_update$', views.PolicyUpdate.as_view(), name='policy-update'),
]