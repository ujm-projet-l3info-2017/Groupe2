# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 22:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_auto_20170319_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fruit',
            name='colour',
            field=models.PositiveSmallIntegerField(choices=[(0, 'red, brown'), (1, 'green-yellow, brown'), (2, 'brown, purple'), (3, 'pink, brown, purple'), (4, 'violet, blue'), (5, 'all'), (6, 'white'), (7, 'orange'), (8, 'yellow'), (9, 'green-yellow'), (10, 'green'), (11, 'blue'), (12, 'violet'), (13, 'purple'), (14, 'pink'), (15, 'magenta'), (16, 'red'), (17, 'dark-red'), (18, 'brown'), (19, 'bronze'), (20, 'silver'), (21, 'black'), (22, 'unknown')]),
        ),
    ]
