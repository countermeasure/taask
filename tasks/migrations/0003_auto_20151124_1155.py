# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20151121_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='time_remaining',
            field=models.PositiveIntegerField(default=15, null=True, blank=True),
            preserve_default=True,
        ),
    ]
