# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-14 08:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20170314_0827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='can_flower',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='plant',
            name='can_fruit',
            field=models.BooleanField(default=False),
        ),
    ]
