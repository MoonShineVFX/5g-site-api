from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^web_demo_places$', views.WebDemonstrationList.as_view(), name='web-demonstration-list'),
    url(r'^web_demo_places/(?P<pk>\d+)$', views.WebDemonstrationDetail.as_view(), name='web-demonstration-detail'),
]