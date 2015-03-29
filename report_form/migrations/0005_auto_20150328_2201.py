# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report_form', '0004_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='report',
        ),
        migrations.AlterField(
            model_name='file',
            name='title',
            field=models.CharField(max_length=128),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='author',
            field=models.CharField(max_length=128),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='date_of_incident',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='short_description',
            field=models.CharField(max_length=750),
            preserve_default=True,
        ),
    ]
