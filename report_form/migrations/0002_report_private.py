# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report_form', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
