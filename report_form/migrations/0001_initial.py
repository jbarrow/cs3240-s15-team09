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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128)),
                ('file', models.FileField(upload_to='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('short_description', models.CharField(max_length=750)),
                ('location', models.CharField(blank=True, max_length=500)),
                ('detailed_description', models.TextField()),
                ('date_of_incident', models.DateField(blank=True, null=True)),
                ('private', models.BooleanField(default=False)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('time_last_modified', models.DateTimeField(auto_now=True)),
                ('AES_key', models.CharField(blank=True, max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('keyword', models.CharField(blank=True, max_length=128, null=True)),
                ('associated_report', models.ForeignKey(to='report_form.Report')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
