# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=128)),
                ('file', models.FileField(upload_to='input/%Y/%m/%d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('short_description', models.CharField(max_length=750)),
                ('location', models.CharField(max_length=500, blank=True)),
                ('detailed_description', models.TextField()),
                ('date_of_incident', models.DateField(null=True, blank=True)),
                ('private', models.BooleanField(default=False)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('time_last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('keyword', models.CharField(max_length=128, null=True, blank=True)),
                ('associated_report', models.ForeignKey(to='report_form.Report')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
