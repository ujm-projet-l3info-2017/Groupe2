# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 22:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_auto_20170319_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fruit',
            name='colour',
            field=models.PositiveSmallIntegerField(choices=[(0, 'red, brown'), (1, 'brown, purple'), (2, 'pink, brown, purple'), (3, 'violet, blue'), (4, 'all'), (5, 'white'), (6, 'orange'), (7, 'yellow'), (8, 'green-yellow'), (9, 'green'), (10, 'blue'), (11, 'violet'), (12, 'purple'), (13, 'pink'), (14, 'magenta'), (15, 'red'), (16, 'dark-red'), (17, 'brown'), (18, 'bronze'), (19, 'silver'), (20, 'black'), (21, 'unknown')]),
        ),
        migrations.AlterField(
            model_name='fruit',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'capsule'), (1, 'cone (winged seeds)'), (2, 'aborted (hybrids) or absent'), (3, 'schizocarp, capsule'), (4, 'samara'), (5, 'unknown')]),
        ),
    ]
