# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('report_form', '0001_initial'),
        ('group_form', '0002_group_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False)),
                ('name', models.CharField(max_length=128, null=True)),
                ('session_token', models.CharField(max_length=255, null=True)),
                ('admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(to='group_form.Group')),
                ('permissions', models.ManyToManyField(to='report_form.Permission')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
