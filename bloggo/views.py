# -*- coding: utf-8 -*-
from django.conf import settings
from django.views.generic import (
    ListView,
    TemplateView as BaseTemplateView,
)

from .models import User, Article


class BloggoMixin:

    def get_context_data(self, **kwargs):
        kwargs.setdefault('aside_user', self.get_aside_user())
        kwargs.setdefault('site_name', getattr(settings, 'SITE_NAME', None))
        kwargs.setdefault('site_tagline',
                          getattr(settings, 'SITE_TAGLINE', None))
        return super().get_context_data(**kwargs)

    def get_aside_user(self):
        return User.objects.filter(is_superuser=True).order_by('id').first()


class TemplateView(BloggoMixin, BaseTemplateView):
    pass


class Home(BloggoMixin, ListView):

    model = Article
    template_name = 'bloggo/home.html'
