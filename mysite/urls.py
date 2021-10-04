from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('apps.article.urls')),
    url(r'^api/', include('apps.index.urls')),
    url(r'^api/', include('apps.tag.urls')),
]
