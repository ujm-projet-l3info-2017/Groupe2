# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 21:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_auto_20170319_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flower',
            name='colour',
            field=models.PositiveSmallIntegerField(choices=[(0, 'brown, purple'), (1, 'pink, brown, purple'), (2, 'violet, blue'), (3, 'All'), (4, 'White'), (5, 'Orange'), (6, 'Yellow'), (7, 'Green-yellow'), (8, 'Green'), (9, 'Blue'), (10, 'Violet'), (11, 'Purple'), (12, 'Pink'), (13, 'Magenta'), (14, 'Red'), (15, 'Dark-red'), (16, 'Brown'), (17, 'Bronze'), (18, 'Silver'), (19, 'Black'), (20, 'unknown')]),
        ),
        migrations.AlterField(
            model_name='fruit',
            name='colour',
            field=models.PositiveSmallIntegerField(choices=[(0, 'brown, purple'), (1, 'pink, brown, purple'), (2, 'violet, blue'), (3, 'All'), (4, 'White'), (5, 'Orange'), (6, 'Yellow'), (7, 'Green-yellow'), (8, 'Green'), (9, 'Blue'), (10, 'Violet'), (11, 'Purple'), (12, 'Pink'), (13, 'Magenta'), (14, 'Red'), (15, 'Dark-red'), (16, 'Brown'), (17, 'Bronze'), (18, 'Silver'), (19, 'Black'), (20, 'unknown')]),
        ),
    ]
