# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-08-05 02:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0200_auto_20210802_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mooring',
            name='mooring_licence',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mooringlicensing.MooringLicence'),
        ),
    ]
