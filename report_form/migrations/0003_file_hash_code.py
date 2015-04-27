# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report_form', '0002_auto_20150426_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='hash_code',
            field=models.CharField(null=True, blank=True, max_length=500),
            preserve_default=True,
        ),
    ]
