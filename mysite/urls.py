from django.conf.urls import url, include

urlpatterns = [
    #url(r'^', include('apps.article.urls')),
    url(r'^', include('apps.index.urls')),
    #url(r'^', include('apps.tag.urls')),
]