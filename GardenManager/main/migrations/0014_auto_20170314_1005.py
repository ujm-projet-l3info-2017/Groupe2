# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-14 10:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20170314_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='common_name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='plant',
            name='scientific_name',
            field=models.CharField(max_length=64),
        ),
    ]
