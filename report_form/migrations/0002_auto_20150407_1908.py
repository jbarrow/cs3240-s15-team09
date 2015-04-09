# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('report_form', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='date_of_incident',
            field=models.DateField(default=datetime.datetime(2015, 4, 7, 23, 8, 11, 948389, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
    ]
