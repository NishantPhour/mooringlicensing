# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-04-08 08:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0287_stickerprintedcontact'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='auto_approve',
            field=models.BooleanField(default=False),
        ),
    ]
