# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-14 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20170314_1005'),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.CharField(max_length=90, primary_key=True, serialize=False, unique=True)),
                ('habit', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='plant',
            name='habit',
        ),
        migrations.AddField(
            model_name='plant',
            name='habits',
            field=models.ManyToManyField(null=True, related_name='plants', to='main.Habit'),
        ),
    ]
