# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-06-04 08:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0143_auto_20210604_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sticker',
            name='status',
            field=models.CharField(choices=[('---', '---'), ('current', 'Current'), ('new_sticker_requested', 'New Sticker Requested'), ('awaiting_sticker', 'Awaiting Sticker'), ('sticker_returned', 'Sticker Returned'), ('sticker_lost', 'Sticker Lost'), ('expired', 'Expired')], default='---', max_length=40),
        ),
    ]