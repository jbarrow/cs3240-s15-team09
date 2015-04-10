# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('userprofile', models.ForeignKey(to='secure_witness.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('short_description', models.CharField(max_length=750)),
                ('location', models.CharField(max_length=500, blank=True)),
                ('detailed_description', models.TextField()),
                ('date_of_incident', models.DateField(null=True, blank=True)),
                ('private', models.BooleanField(default=False)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('time_last_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(to='secure_witness.UserProfile')),
                ('folder', models.ForeignKey(to='report_form.Folder', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('keyword', models.CharField(max_length=128)),
                ('associated_report', models.ForeignKey(to='report_form.Report')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='file',
            name='report',
            field=models.ForeignKey(to='report_form.Report'),
            preserve_default=True,
        ),
    ]
