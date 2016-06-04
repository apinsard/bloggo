# -*- coding: utf-8 -*-
from .base import *  # noqa

DEBUG = True

INSTALLED_APPS.extend([
    'debug_toolbar',
])

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
