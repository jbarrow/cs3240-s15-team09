# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('report_form', '0002_report_private'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='title',
            new_name='short_description',
        ),
        migrations.RemoveField(
            model_name='report',
            name='time',
        ),
        migrations.AddField(
            model_name='report',
            name='date_of_incident',
            field=models.DateField(blank=True, default=datetime.datetime(2015, 3, 26, 22, 11, 7, 246413, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='detailed_description',
            field=models.TextField(default=datetime.datetime(2015, 3, 26, 22, 11, 22, 330276, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='time_created',
            field=models.TimeField(auto_now_add=True, default=datetime.datetime(2015, 3, 26, 22, 11, 25, 364449, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='time_last_modified',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 3, 26, 22, 11, 28, 155609, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to='input/%Y/%m/%d'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='location',
            field=models.CharField(max_length=500, blank=True),
            preserve_default=True,
        ),
    ]
