# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('group_form', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('admin', models.BooleanField(default=False)),
                ('session_token', models.CharField(max_length=255)),
                ('groups', models.ManyToManyField(to='group_form.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
