# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-12 16:17
from __future__ import unicode_literals

import bloggo.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='e-mail address')),
                ('display_name', models.CharField(blank=True, max_length=30, verbose_name='display name')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('picture', models.ImageField(blank=True, upload_to='%Y/users/pictures/', verbose_name='picture')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='birth date')),
                ('short_description', models.CharField(blank=True, max_length=255, verbose_name='short description')),
                ('website', models.URLField(blank=True, verbose_name='website')),
                ('website_name', models.CharField(blank=True, max_length=50, verbose_name='website name')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            managers=[
                ('objects', bloggo.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
                ('pub_date', models.DateTimeField(blank=True, null=True, verbose_name='publication date')),
                ('update_date', models.DateTimeField(blank=True, null=True, verbose_name='is_online')),
                ('is_online', models.BooleanField(default=False, verbose_name='is online')),
                ('teaser', models.TextField(verbose_name='teaser')),
                ('content', models.FileField(upload_to='%Y/articles/', verbose_name='content')),
                ('illustration', models.ImageField(blank=True, upload_to='%Y/illustrations/', verbose_name='illustration')),
                ('illustration_credit', models.CharField(blank=True, max_length=50, verbose_name='illustration credit')),
                ('illustration_credit_url', models.URLField(blank=True, verbose_name='illustration credit link')),
                ('view_count', models.PositiveIntegerField(default=0, verbose_name='view count')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('subscribed_users', models.ManyToManyField(related_name='article_subscriptions', to=settings.AUTH_USER_MODEL, verbose_name='subscribed users')),
            ],
            options={
                'verbose_name_plural': 'articles',
                'verbose_name': 'article',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='ip address')),
                ('action', models.CharField(choices=[('view_article', 'viewed article'), ('comment_article', 'commented article'), ('upvote_comment', 'upvoted comment'), ('downvote_comment', 'downvoted comment'), ('report_comment', 'reported comment')], max_length=50, verbose_name='action')),
                ('when', models.DateTimeField(auto_now_add=True, verbose_name='when')),
                ('target_id', models.PositiveSmallIntegerField(verbose_name='target')),
                ('comment', models.TextField(blank=True, verbose_name='comment')),
                ('target_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='target type')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name_plural': 'logs',
                'verbose_name': 'log',
            },
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction', models.CharField(blank=True, choices=[('must_read', 'Must read'), ('interesting', 'Interesting'), ('fuzzy', 'Fuzzy'), ('outdated', 'Outdated'), ('mistaking', 'Mistaking')], max_length=20, verbose_name='reaction')),
                ('comment', models.TextField(blank=True, verbose_name='comment')),
                ('posted_on', models.DateTimeField(auto_now_add=True, verbose_name='posted on')),
                ('is_valid', models.NullBooleanField(verbose_name='is valid')),
                ('up_votes', models.PositiveSmallIntegerField(default=0, verbose_name='up votes')),
                ('down_votes', models.PositiveSmallIntegerField(default=0, verbose_name='down votes')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bloggo.Article', verbose_name='article')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='author')),
            ],
            options={
                'verbose_name_plural': 'reactions',
                'verbose_name': 'reaction',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('article_count', models.PositiveSmallIntegerField(default=0, verbose_name='article count')),
                ('article_view_count', models.PositiveIntegerField(default=0, verbose_name='article view count')),
            ],
            options={
                'verbose_name_plural': 'tags',
                'verbose_name': 'tag',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='bloggo.Tag', verbose_name='tags'),
        ),
    ]
