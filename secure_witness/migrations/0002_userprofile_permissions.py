# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report_form', '0003_permission'),
        ('secure_witness', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='permissions',
            field=models.ManyToManyField(to='report_form.Permission'),
            preserve_default=True,
        ),
    ]