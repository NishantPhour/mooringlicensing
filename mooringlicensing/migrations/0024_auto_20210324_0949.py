# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-03-24 01:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0023_merge_20210324_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='emailuser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
