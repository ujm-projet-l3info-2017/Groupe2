# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-09 10:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0048_auto_20170409_1008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='session',
        ),
        migrations.DeleteModel(
            name='Session',
        ),
    ]
