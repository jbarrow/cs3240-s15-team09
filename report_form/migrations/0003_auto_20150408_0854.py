# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report_form', '0002_auto_20150407_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='date_of_incident',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
