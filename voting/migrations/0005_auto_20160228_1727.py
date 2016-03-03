# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-28 17:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0004_remove_customuser_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='district',
            name='state',
        ),
        migrations.RemoveField(
            model_name='seat',
            name='district',
        ),
        migrations.RemoveField(
            model_name='ward',
            name='seat',
        ),
        migrations.DeleteModel(
            name='District',
        ),
        migrations.DeleteModel(
            name='Seat',
        ),
        migrations.DeleteModel(
            name='State',
        ),
        migrations.DeleteModel(
            name='Ward',
        ),
    ]
