# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^about/$',
        views.TemplateView.as_view(template_name='bloggo/about.html'),
        name='about'),
]
