# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-06-04 05:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0139_auto_20210604_1105'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StickersDocument',
            new_name='StickerPrintingBatch',
        ),
        migrations.RenameField(
            model_name='sticker',
            old_name='stickers_document',
            new_name='sticker_printing_batch',
        ),
        migrations.AlterField(
            model_name='sticker',
            name='status',
            field=models.CharField(choices=[('awaiting_exported', 'Awaiting Exported'), ('awaiting_printed', 'Awaiting Printed'), ('current', 'Current'), ('new_sticker_requested', 'New Sticker Requested'), ('awaiting_sticker', 'Awaiting Sticker'), ('sticker_returned', 'Sticker Returned'), ('sticker_lost', 'Sticker Lost'), ('expired', 'Expired')], default='current', max_length=40),
        ),
    ]
