# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 21:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_auto_20170319_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flower',
            name='colour',
            field=models.PositiveSmallIntegerField(choices=[(0, 'brown, purple'), (1, 'pink, brown, purple'), (2, 'violet, blue'), (3, 'all'), (4, 'white'), (5, 'orange'), (6, 'yellow'), (7, 'green-yellow'), (8, 'green'), (9, 'blue'), (10, 'violet'), (11, 'purple'), (12, 'pink'), (13, 'magenta'), (14, 'red'), (15, 'dark-red'), (16, 'brown'), (17, 'bronze'), (18, 'silver'), (19, 'black'), (20, 'unknown')]),
        ),
        migrations.AlterField(
            model_name='fruit',
            name='colour',
            field=models.PositiveSmallIntegerField(choices=[(0, 'brown, purple'), (1, 'pink, brown, purple'), (2, 'violet, blue'), (3, 'all'), (4, 'white'), (5, 'orange'), (6, 'yellow'), (7, 'green-yellow'), (8, 'green'), (9, 'blue'), (10, 'violet'), (11, 'purple'), (12, 'pink'), (13, 'magenta'), (14, 'red'), (15, 'dark-red'), (16, 'brown'), (17, 'bronze'), (18, 'silver'), (19, 'black'), (20, 'unknown')]),
        ),
    ]
