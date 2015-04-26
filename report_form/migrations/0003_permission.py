# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_form', '0002_group_users'),
        ('secure_witness', '0001_initial'),
        ('report_form', '0002_auto_20150422_0928'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('groups', models.ManyToManyField(to='group_form.Group')),
                ('profiles', models.ManyToManyField(to='secure_witness.UserProfile')),
                ('report', models.ForeignKey(to='report_form.Report')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
