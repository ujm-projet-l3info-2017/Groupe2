# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-14 08:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20170314_0822'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plant',
            name='spread',
        ),
        migrations.AddField(
            model_name='plant',
            name='spread_max',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='plant',
            name='spread_min',
            field=models.FloatField(null=True),
        ),
    ]
