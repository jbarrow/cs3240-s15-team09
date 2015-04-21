# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '0001_initial'),
        ('group_form', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(to='secure_witness.UserProfile'),
            preserve_default=True,
        ),
    ]
