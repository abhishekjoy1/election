# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-04 12:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0009_seat_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='state',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='voting.State'),
            preserve_default=False,
        ),
    ]
