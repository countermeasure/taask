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
                ('context', models.CharField(unique=True, max_length=50)),
            ],
            options={
                'ordering': ['context'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.PositiveIntegerField(unique=True)),
                ('priority', models.CharField(unique=True, max_length=20)),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('project', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ['project'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('completed', models.DateTimeField(null=True, blank=True)),
                ('description', models.CharField(max_length=200)),
                ('deadline', models.DateField(null=True, blank=True)),
                ('repeat_details', models.CharField(max_length=200, blank=True)),
                ('repeat_ends', models.DateField(null=True, verbose_name=b'Repeats until', blank=True)),
                ('repeat_every', models.PositiveIntegerField(null=True, blank=True)),
                ('repeat_next', models.DateField(null=True, verbose_name=b'Next occurance', blank=True)),
                ('repeat_units', models.CharField(blank=True, max_length=20, verbose_name=b'Create copies', choices=[(b'daily', b'Daily'), (b'weekly', b'Weekly'), (b'monthly', b'Monthly'), (b'yearly', b'Yearly')])),
                ('notes', models.TextField(blank=True)),
                ('scheduled', models.DateField(null=True, verbose_name=b'Postpone until', blank=True)),
                ('time_remaining', models.PositiveIntegerField(null=True, blank=True)),
                ('time_spent', models.PositiveIntegerField(null=True, blank=True)),
                ('underway', models.BooleanField(default=False)),
                ('view', models.CharField(max_length=50, choices=[(b'inbox', b'Inbox'), (b'today', b'Today'), (b'next', b'Next'), (b'scheduled', b'Scheduled'), (b'recurring', b'Recurring'), (b'someday', b'Someday'), (b'completed', b'Completed'), (b'rubbish', b'Rubbish')])),
                ('context', models.ManyToManyField(to='tasks.Context', null=True, blank=True)),
                ('priority', models.ForeignKey(blank=True, to='tasks.Priority', null=True)),
                ('project', models.ForeignKey(blank=True, to='tasks.Project', null=True)),
                ('task', models.ForeignKey(related_name='child_tasks', blank=True, to='tasks.Task', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
