# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-03-09 03:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0002_waitinglistapplication'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='data',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='schema',
        ),
    ]