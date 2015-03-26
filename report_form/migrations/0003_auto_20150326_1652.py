# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report_form', '0002_report_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to='input/%Y/%m/%d'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='location',
            field=models.CharField(blank=True, max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='time',
            field=models.DateTimeField(blank=True),
            preserve_default=True,
        ),
    ]
