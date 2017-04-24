# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-24 12:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0049_auto_20170409_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='creation_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='main.User'),
        ),
    ]