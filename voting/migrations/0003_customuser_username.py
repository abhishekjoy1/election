# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-28 16:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0002_auto_20160228_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(default=123456, max_length=40, unique=True),
            preserve_default=False,
        ),
    ]
