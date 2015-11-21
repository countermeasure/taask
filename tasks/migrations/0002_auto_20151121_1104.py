# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='view',
            field=models.CharField(default=b'inbox', max_length=50, choices=[(b'inbox', b'Inbox'), (b'today', b'Today'), (b'next', b'Next'), (b'scheduled', b'Scheduled'), (b'recurring', b'Recurring'), (b'someday', b'Someday'), (b'completed', b'Completed'), (b'rubbish', b'Rubbish')]),
            preserve_default=True,
        ),
    ]
