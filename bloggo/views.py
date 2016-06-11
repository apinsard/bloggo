# -*- coding: utf-8 -*-
from django.views.generic import ListView

from .models import Article


class Home(ListView):

    model = Article
    template_name = 'bloggo/home.html'
