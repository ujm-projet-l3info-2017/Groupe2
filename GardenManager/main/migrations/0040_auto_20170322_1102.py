# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 11:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_auto_20170322_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fruittype',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'berry'), (1, 'capsule'), (2, 'cone'), (3, 'aborted or absent'), (4, 'schizocarp'), (5, 'samara'), (6, 'cypsela'), (7, 'follicle'), (8, 'aggregate fruit'), (9, 'unknown')]),
        ),
    ]
