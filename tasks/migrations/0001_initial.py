# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Context',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('context', models.CharField(max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('priority', models.CharField(max_length=20, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('project', models.CharField(max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=200)),
                ('notes', models.TextField(null=True)),
                ('view', models.CharField(max_length=50)),
                ('time', models.PositiveIntegerField(null=True)),
                ('due', models.DateTimeField(null=True)),
                ('scheduled', models.DateTimeField(null=True)),
                ('status', models.CharField(max_length=20)),
                ('active', models.BooleanField(default=False)),
                ('frequency', models.CharField(max_length=50, null=True)),
                ('ends', models.DateTimeField(null=True)),
                ('context', models.ForeignKey(to='tasks.Context', null=True)),
                ('priority', models.ForeignKey(to='tasks.Priority', null=True)),
                ('project', models.ForeignKey(to='tasks.Project', null=True)),
                ('task', models.ForeignKey(related_name='child_tasks', to='tasks.Task', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
