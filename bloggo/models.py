# -*- coding: utf-8 -*-
from datetime import date

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.forms.utils import flatatt
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields['is_staff'] is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields['is_superuser'] is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    email = models.EmailField(
        unique=True,
        verbose_name=_("e-mail address"),
    )
    display_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name=_("display name"),
    )
    first_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name=_("first name"),
    )
    last_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name=_("last name"),
    )
    is_staff = models.BooleanField(
        verbose_name=_("staff status"),
        default=False,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("active"),
    )
    date_joined = models.DateTimeField(
        verbose_name=_("date joined"),
        default=timezone.now,
    )
    picture = models.ImageField(
        upload_to='%Y/users/pictures/',
        blank=True,
        verbose_name=_("picture"),
    )
    birth_date = models.DateField(
        blank=True, null=True,
        verbose_name=_("birth date"),
    )
    short_description = models.CharField(
        max_length=255,
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

    def __str__(self):
        return self.email

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name).strip()

    def get_short_name(self):
        return self.display_name or self.get_full_name() or _("Anonymous")
    get_short_name.short_description = _("display name")

    def get_website_link(self, attrs=None):
        if not self.website:
            return None
        if attrs is None:
            attrs = {'target': '_blank'}
        attrs['href'] = self.website
        website_name = self.website_name or self.website
        return format_html('<a{}>{}</a>', flatatt(attrs), website_name)
    get_website_link.short_description = _("website")

    def get_age(self):
        bday = self.birth_date
        if not bday:
            return None
        today = date.today()
        return today.year - bday.year - (
            (today.month, today.day) < (bday.month, bday.day))


class Tag(models.Model):

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("name"),
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name=_("slug")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("description"),
    )
    article_count = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("article count")
    )
    article_view_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("article view count"),
    )

    def __str__(self):
        return self.name


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
        settings.AUTH_USER_MODEL, models.PROTECT,
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
    teaser = models.TextField(
        verbose_name=_("teaser"),
    )
    content = models.FileField(
        upload_to='%Y/articles/',
        verbose_name=_("content")
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_("tags"),
    )
    illustration = models.ImageField(
        upload_to='%Y/illustrations/',
        blank=True,
        verbose_name=_("illustration"),
    )
    illustration_credit = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("illustration credit"),
    )
    illustration_credit_url = models.URLField(
        blank=True,
        verbose_name=_("illustration credit link")
    )
    view_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("view count"),
    )
    subscribed_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='article_subscriptions',
        verbose_name=_("subscribed users"),
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


class Reaction(models.Model):

    class Meta:
        verbose_name = _("reaction")
        verbose_name_plural = _("reactions")

    REACTION_CHOICES = [
        ('must_read', _("Must read")),
        ('interesting', _("Interesting")),
        ('fuzzy', _("Fuzzy")),
        ('outdated', _("Outdated")),
        ('mistaking', _("Mistaking")),
    ]

    article = models.ForeignKey(
        Article, models.CASCADE,
        verbose_name=_("article"),
    )
    reaction = models.CharField(
        max_length=20,
        blank=True,
        choices=REACTION_CHOICES,
        verbose_name=_("reaction"),
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_("comment"),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.SET_NULL,
        blank=True, null=True,
        verbose_name=_("author"),
    )
    posted_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("posted on"),
    )
    is_valid = models.NullBooleanField(
        verbose_name=_("is valid"),
    )
    up_votes = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("up votes"),
    )
    down_votes = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("down votes"),
    )

    def __str__(self):
        return '#{}'.format(self.pk)

    def clean(self):
        super().clean()
        if not self.reaction and not self.comment:
            raise ValidationError(
                _("Please submit at least your reaction or a comment.")
            )


class Log(models.Model):

    class Meta:
        verbose_name = _("log")
        verbose_name_plural = _("logs")

    ACTION_CHOICES = [
        ('view_article', _("viewed article")),
        ('comment_article', _("commented article")),
        ('upvote_comment', _("upvoted comment")),
        ('downvote_comment', _("downvoted comment")),
        ('report_comment', _("reported comment")),
    ]

    ip_address = models.GenericIPAddressField(
        verbose_name=_("ip address"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.SET_NULL,
        blank=True, null=True,
        verbose_name=_("user"),
    )
    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES,
        verbose_name=_("action"),
    )
    when = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("when"),
    )
    target_type = models.ForeignKey(
        ContentType, models.CASCADE,
        verbose_name=_("target type"),
    )
    target_id = models.PositiveSmallIntegerField(
        verbose_name=_("target"),
    )
    target = GenericForeignKey('target_type', 'target_id')
    comment = models.TextField(
        blank=True,
        verbose_name=_("comment"),
    )

    def __str__(self):
        message = _("{client} {action} \"{target}\" on {when}")
        return message.format(
            client=self.get_client_info(),
            action=self.get_action_display(),
            target_type=self.target_type._meta.verbose_name,
            target=self.target,
            when=date_format(self.when, 'DATETIME_FORMAT'),
        )
