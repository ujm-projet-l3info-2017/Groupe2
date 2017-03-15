# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-15 13:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20170315_1339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ground',
            name='type',
        ),
        migrations.AddField(
            model_name='ground',
            name='ground',
            field=models.PositiveSmallIntegerField(choices=[(0, 'all'), (1, 'acidic'), (2, 'bog'), (3, 'well-drained'), (4, 'humus rich'), (5, 'alkaline'), (6, 'rocky or gravelly or dry'), (7, 'unknown')], null=True),
        ),
    ]
