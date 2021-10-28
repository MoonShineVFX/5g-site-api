from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^demo_places$', views.DemonstrationList.as_view(), name='demonstration-list'),
    url(r'^demo_places/(?P<pk>\d+)$', views.DemonstrationDetail.as_view(), name='demonstration-detail'),
    url(r'^demo_place_create$', views.DemonstrationCreate.as_view(), name='demonstration-create'),
    url(r'^demo_place_update$', views.DemonstrationUpdate.as_view(), name='demonstration-update'),

    url(r'^demo_place_image_upload$', views.ImageUpload.as_view(), name='emonstration-image-upload'),
    url(r'^demo_place_file_upload$', views.FileUpload.as_view(), name='emonstration-file-upload'),

    url(r'^web_demo_places$', views.WebDemonstrationList.as_view(), name='web-demonstration-list'),
    url(r'^web_demo_places/(?P<pk>\d+)$', views.WebDemonstrationDetail.as_view(), name='web-demonstration-detail'),
]