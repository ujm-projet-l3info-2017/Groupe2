# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-14 08:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20170313_1430'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plant',
            name='height',
        ),
        migrations.AddField(
            model_name='plant',
            name='height_max',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='plant',
            name='height_min',
            field=models.FloatField(null=True),
        ),
    ]
