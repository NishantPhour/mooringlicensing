# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-06-02 03:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mooringlicensing.components.proposals.models


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0129_auto_20210531_1703'),
    ]

    operations = [
        migrations.CreateModel(
            name='StickersDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
                ('_file', models.FileField(max_length=512, upload_to=mooringlicensing.components.proposals.models.update_sticker_doc_filename)),
                ('emailed_datetime', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='annualadmissionapplication',
            name='stickers_document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mooringlicensing.StickersDocument'),
        ),
        migrations.AddField(
            model_name='authoriseduserapplication',
            name='stickers_document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mooringlicensing.StickersDocument'),
        ),
        migrations.AddField(
            model_name='mooringlicenceapplication',
            name='stickers_document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mooringlicensing.StickersDocument'),
        ),
    ]
