# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import UserChangeForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['-date_joined']
    list_display = [
        'email', 'get_short_name', 'get_website_link', 'date_joined',
        'is_active',
    ]
    form = UserChangeForm
    fieldsets = [
        (None, {'fields': [
            'display_name', 'email', 'password', 'picture',
            'short_description', 'website', 'website_name',
        ]}),
        (_("Personal info"), {'fields': [
            'first_name', 'last_name', 'birth_date',
        ]}),
        (_("Permissions"), {'fields': [
            'is_active', 'is_staff', 'is_superuser', 'groups',
            'user_permissions',
        ]}),
        (_("Important dates"), {'fields': [
            'last_login', 'date_joined',
        ]}),
    ]

    def has_add_permission(self, request):
        return False
