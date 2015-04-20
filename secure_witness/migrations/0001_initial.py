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
                ('user', models.OneToOneField(serialize=False, to=settings.AUTH_USER_MODEL, primary_key=True)),
                ('name', models.CharField(null=True, max_length=128)),
                ('session_token', models.CharField(null=True, max_length=255)),
                ('admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(to='group_form.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
