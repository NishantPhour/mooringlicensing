# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-07-05 04:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0186_remove_sticker_vessel_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvalhistory',
            name='vessel_ownership',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mooringlicensing.VesselOwnership'),
        ),
    ]
