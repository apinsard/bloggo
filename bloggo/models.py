# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Author(models.Model):

    class Meta:
        verbose_name = _("author")
        verbose_name_plural = _("authors")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        blank=True, null=True,
        verbose_name=_("user account"),
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name=_("first name"),
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("last name"),
    )
    email = models.EmailField(
        blank=True,
        verbose_name=_("e-mail"),
    )
    birth_date = models.DateField(
        blank=True, null=True,
        verbose_name=_("birth date"),
    )
    short_description = models.CharField(
        blank=True,
        verbose_name=_("short description"),
    )
    website = models.URLField(
        blank=True,
        verbose_name=_("website"),
    )
    website_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("website name"),
    )


class Article(models.Model):

    class Meta:
        verbose_name = _("article")
        verbose_name_plural = _("articles")

    title = models.CharField(
        max_length=200,
        verbose_name=_("title"),
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name=_("slug"),
    )
    author = models.ForeignKey(
        Author, models.PROTECT,
        blank=True, null=True,
        verbose_name=_("author"),
    )
    pub_date = models.DateTimeField(
        blank=True, null=True,
        verbose_name=_("publication date"),
    )
    update_date = models.DateTimeField(
        blank=True, null=True,
        verbose_name=_("is_online")
    )
    is_online = models.BooleanField(
        default=False,
        verbose_name=_("is online"),
    )
    content = models.TextField(
        verbose_name=_("content"),
    )

    def __str__(self):
        return self.slug

    def clean(self):
        super().clean()
        if self.is_online and not self.pub_date:
            self.pub_date = timezone.now()
        if self.update_date:
            if not self.pub_date or self.pub_date >= self.update_date:
                self.update_date = None

    def get_last_modified(self):
        return self.update_date or self.pub_date
