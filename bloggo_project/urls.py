# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('bloggo.urls')),
]

if settings.DEBUG:
    from django.views.static import serve as static_serve
    urlpatterns.append(
        url(r'^__media__/(?P<path>.*)$',
            static_serve, {
                'document_root': settings.MEDIA_ROOT,
                'show_indexes': True
            }))
