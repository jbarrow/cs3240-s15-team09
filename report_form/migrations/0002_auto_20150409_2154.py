# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report_form', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='folder',
            field=models.ForeignKey(blank=True, null=True, to='report_form.Folder'),
            preserve_default=True,
        ),
    ]
