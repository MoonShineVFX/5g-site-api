from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^get_token$', views.ObtainTokenView.as_view(), name='get-token'),
]