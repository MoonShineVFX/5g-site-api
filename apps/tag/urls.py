from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^common$', views.CommonView.as_view(), name='common'),

    url(r'^tags_and_categories$', views.TagAndCategoryList.as_view(), name='tag-list'),
    url(r'^tag_create$', views.TagCreate.as_view(), name='tag-create'),
    url(r'^tag_update$', views.TagUpdate.as_view(), name='tag-update'),
    url(r'^tag_delete$', views.TagDelete.as_view(), name='tag-delete'),
]