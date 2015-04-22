# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '0001_initial'),
        ('report_form', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='author',
            field=models.ForeignKey(to='secure_witness.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='folder',
            field=models.ForeignKey(to='report_form.Folder', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='folder',
            name='userprofile',
            field=models.ForeignKey(to='secure_witness.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='report',
            field=models.ForeignKey(to='report_form.Report'),
            preserve_default=True,
        ),
    ]
