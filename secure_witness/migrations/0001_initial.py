# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('group_form', '0001_initial'),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128, null=True)),
                ('session_token', models.CharField(max_length=255, null=True)),
                ('admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(to='group_form.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
