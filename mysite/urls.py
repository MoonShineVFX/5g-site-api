from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('apps.article.urls')),
    url(r'^api/', include('apps.index.urls')),
    url(r'^api/', include('apps.tag.urls')),
    url(r'^api/', include('apps.demonstration.urls')),
    url(r'^api/', include('apps.policy.urls')),
    url(r'^api/', include('apps.user.urls')),
]
