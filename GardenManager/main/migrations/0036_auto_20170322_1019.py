# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 10:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_auto_20170320_1622'),
    ]

    operations = [
        migrations.CreateModel(
            name='FruitType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'capsule'), (1, 'cone'), (2, 'aborted or absent'), (3, 'schizocarp'), (4, 'samara'), (5, 'cypsela'), (6, 'follicle'), (7, 'aggregate fruit'), (8, 'unknown')])),
            ],
        ),
        migrations.AlterField(
            model_name='fruit',
            name='months',
            field=models.ManyToManyField(related_name='fruits', to='main.Month'),
        ),
        migrations.AddField(
            model_name='fruit',
            name='types',
            field=models.ManyToManyField(related_name='fruits', to='main.FruitType'),
        ),
    ]
